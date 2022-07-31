from django.urls import path
from apis.youtube.views import (
    YoutubeVideoListAPIView
)

urlpatterns = [
    path('', YoutubeVideoListAPIView.as_view(), name="youtube_video_information"),
]
