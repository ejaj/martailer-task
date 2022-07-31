from rest_framework import generics
from rest_framework import filters
from youtube.models import YoutubeVideos

from youtube.serializers import YoutubeVideosSerializer
import logging

logger = logging.getLogger()


class YoutubeVideoListAPIView(generics.ListAPIView):
    """
    Youtube Video List API View
    """
    queryset = YoutubeVideos.objects.all()
    serializer_class = YoutubeVideosSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('tags__name',)
