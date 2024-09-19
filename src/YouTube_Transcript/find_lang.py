from youtube_transcript_api import YouTubeTranscriptApi
from get_video_info import extract_video_id

video_id = extract_video_id("https://www.youtube.com/watch?v=pHdzv1NfZRM")

transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
print(transcript_list)

