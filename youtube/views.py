from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from .models import YouTubeLink, Transcript
from .serializers import YouTubeLinkSerializer
import re

class YouTubeTranscriptAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        link = request.data.get('link')
        language = request.data.get('language')

        # 유튜브 링크에서 동영상 ID 추출
        video_id = self.extract_video_id(link)
        
        if not video_id:
            return Response({"error": "Invalid YouTube link."}, status=status.HTTP_400_BAD_REQUEST)

        # 이미 저장된 링크인지 확인
        youtube_link, created = YouTubeLink.objects.get_or_create(link=link, video_id=video_id, language=language)

        if not created:
            # 이미 저장된 링크가 있을 경우 해당 링크의 자막 반환
            serializer = YouTubeLinkSerializer(youtube_link)
            return Response(serializer.data, status=status.HTTP_200_OK)

        try:
            # YouTubeTranscriptApi를 사용해 자막 가져오기
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=[f'{language}'])

            # 자막 저장
            for item in transcript_data:
                Transcript.objects.create(
                    youtube_link=youtube_link,
                    text=item['text'],
                    start=item['start'],
                    duration=item['duration']
                )

            # 저장된 링크와 자막 반환
            serializer = YouTubeLinkSerializer(youtube_link)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def extract_video_id(url):
        # 유튜브 URL에서 비디오 ID 추출
        video_id_match = re.search(r"(?:v=|/)([0-9A-Za-z_-]{11}).*", url)
        if video_id_match:
            return video_id_match.group(1)
        else:
            raise ValueError("Invalid YouTube URL")