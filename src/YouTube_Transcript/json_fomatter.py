# 필요한 모듈과 함수들을 가져옵니다.
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from get_video_info import extract_video_id, get_video_title
from get_timestamp_title import extract_timestamps_from_description
import os
import re
import json
from dotenv import load_dotenv

def extract_transcripts_as_json(url):
    # 기본적인 영상의 정보 추출
    video_id = extract_video_id(url)
    title = get_video_title(url)

    # 자막 가져오기
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # 문장 단위로 합치기
    merged_transcript = merge_transcript_sentences(transcript)

    # 파일로 저장 (필요한 경우)
    formatter = JSONFormatter()
    json_formatted = formatter.format_transcript(merged_transcript)

    # 파일로 저장
    sanitized_title = sanitize_filename(title)
    output_folder = "./src/Transcripts/"
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, sanitized_title + '.json')
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_formatted)

    # 자막의 리스트를 반환
    return merged_transcript

def merge_transcript_sentences(transcript):
    merged_transcript = []
    buffer_text = ''
    buffer_start = None
    buffer_duration = 0.0

    # 문장 끝을 나타내는 구두점
    sentence_endings = '.?!'

    for entry in transcript:
        text = entry['text']
        start = entry['start']
        duration = entry['duration']

        if buffer_start is None:
            buffer_start = start

        if buffer_text:
            buffer_text += ' ' + text
        else:
            buffer_text = text

        buffer_duration += duration

        # 문장의 끝인지 확인
        if text.strip() and text.strip()[-1] in sentence_endings:
            merged_entry = {
                'text': buffer_text.strip(),
                'start': buffer_start,
                'duration': buffer_duration
            }
            merged_transcript.append(merged_entry)
            buffer_text = ''
            buffer_start = None
            buffer_duration = 0.0

    # 남은 텍스트가 있으면 추가
    if buffer_text:
        merged_entry = {
            'text': buffer_text.strip(),
            'start': buffer_start,
            'duration': buffer_duration
        }
        merged_transcript.append(merged_entry)

    return merged_transcript

def create_timestamp_transcript_dict(timestamps, transcripts):
    """
    timestamps: list of (timestamp_in_seconds, title) tuples, sorted by timestamp
    transcripts: list of transcript entries, each is a dict with 'text', 'start', 'duration'

    Returns a dictionary where keys are timestamps and values are lists of transcript entries.
    """
    timestamp_transcript_dict = {}

    # 타임스탬프만 추출하여 리스트로 만듭니다.
    timestamp_seconds = [ts for ts, _ in timestamps]

    num_transcripts = len(transcripts)
    transcript_index = 0

    for i, current_timestamp in enumerate(timestamp_seconds):
        if i + 1 < len(timestamp_seconds):
            next_timestamp = timestamp_seconds[i + 1]
        else:
            next_timestamp = None  # 마지막 타임스탬프

        entries = []

        # 자막 인덱스를 순회하면서 해당 구간의 자막을 수집합니다.
        while transcript_index < num_transcripts:
            transcript_entry = transcripts[transcript_index]
            start_time = transcript_entry['start']

            if start_time < current_timestamp:
                # 현재 타임스탬프보다 시작 시간이 이르면 스킵
                transcript_index += 1
                continue
            elif next_timestamp is not None and start_time >= next_timestamp:
                # 다음 타임스탬프 이후면 현재 구간 종료
                break
            else:
                # 현재 타임스탬프 구간에 해당하는 자막
                entries.append(transcript_entry)
                transcript_index += 1

        # 타임스탬프를 키로 하고 자막 리스트를 값으로 추가
        timestamp_transcript_dict[current_timestamp] = entries

    return timestamp_transcript_dict

# 파일 이름에서 허용되지 않는 문자 제거
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)

if __name__ == '__main__':
    # 영상 URL을 설정합니다.
    video_url = "https://www.youtube.com/watch?v=IHZwWFHWa-w&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi&index=2"

    # API 키를 .env 파일에서 불러오기 (get_timestamp_title.py에서 사용)
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")  # .env 파일에 저장된 키를 불러옴

    # 영상 ID와 제목을 추출합니다.
    video_id = extract_video_id(video_url)
    title = get_video_title(video_url)

    # 타임스탬프와 제목을 추출합니다.
    timestamps = extract_timestamps_from_description(video_id, api_key)

    # 자막을 가져오고 문장 단위로 병합합니다.
    merged_transcripts = extract_transcripts_as_json(video_url)

    # 타임스탬프와 자막을 매핑하는 딕셔너리를 생성합니다.
    timestamp_transcript_dict = create_timestamp_transcript_dict(timestamps, merged_transcripts)

    # 결과 출력 (필요한 경우)
    for ts in sorted(timestamp_transcript_dict.keys()):
        print(f"Timestamp: {ts} seconds")
        for entry in timestamp_transcript_dict[ts]:
            print(f" - {entry['text']} (Start: {entry['start']}, Duration: {entry['duration']})")
        print("\n")
