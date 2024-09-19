"""
youtube data api v3를 사용하여 유튜브의 타임 스탬프 제목을 추출
https://developers.google.com/youtube/v3/getting-started?hl=ko
"""
import os
from googleapiclient.discovery import build
import re
from dotenv import load_dotenv
from get_video_info import extract_video_id

# .env 파일 로드
load_dotenv()

def extract_timestamps_from_description(video_id, api_key):
    # YouTube Data API 클라이언트 생성
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # 비디오 정보 요청
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    
    # 비디오 설명 추출
    description = response['items'][0]['snippet']['description']
    
    # 정규식 패턴: MM:SS - Title 형태의 텍스트를 추출
    pattern = r"(\d{1,2}:\d{2})\s*-\s*(.+)"
    
    # 타임스탬프와 제목을 추출
    timestamps = []

    for match in re.finditer(pattern, description):
        time_str, title = match.groups()
        
        # MM:SS 형식을 초로 변환
        minutes, seconds = map(int, time_str.split(':'))
        total_seconds = minutes * 60 + seconds
        
        timestamps.append((total_seconds, title))
    
    return timestamps



if __name__ == "__main__":
    # API 키를 .env 파일에서 불러오기
    api_key = os.getenv("YOUTUBE_API_KEY")  # .env 파일에 저장된 키를 불러옴

    video_url = "https://www.youtube.com/watch?v=IHZwWFHWa-w&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi&index=2"
    # video_url = "https://www.youtube.com/watch?v=AeRwohPuUHQ"
    video_id = extract_video_id(video_url)
    
    timestamps = extract_timestamps_from_description(video_id, api_key)
    print(timestamps)
    
    # for time, title in timestamps:
    #     print(f"{time} - {title}")
