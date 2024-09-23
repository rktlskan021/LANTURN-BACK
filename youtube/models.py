from django.db import models

language_list = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('de', 'German'),
    ('it', 'Italian'),
    ('pt', 'Portuguese'),
    ('ru', 'Russian'),
    ('zh', 'Chinese'),
    ('ja', 'Japanese'),
    ('ko', 'Korean'),
    ('ar', 'Arabic'),
    ('hi', 'Hindi'),
    ('vi', 'Vietnamese'),
    ('th', 'Thai'),
]

class YouTubeLink(models.Model):
    link = models.URLField()  # 유튜브 링크 필드
    video_id = models.CharField(max_length=50)  # 동영상 ID
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간
    language = models.CharField(max_length=10, choices=language_list) # 언어 코드

    class Meta:
        unique_together = ('video_id', 'language')  # video_id와 language의 조합을 고유하게 설정

    def __str__(self):  
        return f"{self.link}/{self.language}"


class Transcript(models.Model):
    youtube_link = models.ForeignKey(YouTubeLink, related_name='transcripts', on_delete=models.CASCADE)  # 링크와 연결
    text = models.TextField()  # 자막 텍스트
    start = models.FloatField()  # 자막 시작 시간
    duration = models.FloatField()  # 자막 지속 시간

    def __str__(self):
        return f"{self.youtube_link} - {self.text[:30]}..."
