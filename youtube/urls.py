from django.urls import path, include, re_path
from rest_framework import routers
from .views import YouTubeTranscriptAPIView

urlpatterns = [
    path('get-transcript/', YouTubeTranscriptAPIView.as_view())
]