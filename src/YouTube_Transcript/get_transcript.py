import re
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from get_video_info import extract_video_id, get_video_title

def save_transcript_to_file(url, output_folder):
    try:
        video_id = extract_video_id(url)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'], preserve_formatting=True)
        
        # 포매터를 사용해 텍스트 형식으로 변환
        formatter = TextFormatter()
        transcript_text = formatter.format_transcript(transcript)

        # 유튜브 제목으로 파일 이름 설정
        video_title = get_video_title(url)
        safe_title = re.sub(r'[\\/*?:"<>|]', "", video_title)  # 파일명에 사용할 수 없는 문자는 제거
        file_name = f"{safe_title}_script.txt"
        file_path = os.path.join(output_folder, file_name)

        # 폴더가 존재하지 않으면 생성
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 텍스트 파일로 저장
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(transcript_text)
        
        print(f"Transcript saved to {file_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":

    # 테스트용 URL
    youtube_url = "https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi"

    # youtube_transcripts 폴더 경로
    output_folder = os.path.join("./src/YouTube_Transcript/", "youtube_transcripts")
    save_transcript_to_file(youtube_url, output_folder)

