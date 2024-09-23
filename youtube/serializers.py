from rest_framework import serializers
from .models import YouTubeLink, Transcript

class TranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transcript
        fields = ['text', 'start', 'duration']


class YouTubeLinkSerializer(serializers.ModelSerializer):
    transcripts = TranscriptSerializer(many=True, read_only=True)  # 자막을 포함하도록 설정
    class Meta:
        model = YouTubeLink
        fields = '__all__'
