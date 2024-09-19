"""
유튜브 영상의 제목 추출 
"""

import re
from pytube import YouTube

def extract_video_id(url):
    # 유튜브 URL에서 비디오 ID 추출
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def get_video_title(url):
    yt = YouTube(url)
    title = yt.title
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    return safe_title


if __name__ == "__main__":
    # 예시 유튜브 URL
    video_url = "https://www.youtube.com/watch?v=aircAruvnKk&list=PLZHQObOWTQDNU6R1_67000Dx_ZCJB-3pi"
    
    video_id = extract_video_id(video_url)  # output: aircAruvnKk
    video_title = get_video_title(video_url)  # output: But what is a neural network? | Chapter 1, Deep learning

    print(f"id: {video_id},  title: {video_title}")
