from rest_framework import serializers
from youtube.models import YoutubeVideos, VideoStats
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


class VideoStatsSerializer(serializers.ModelSerializer):
    """
    Videos Stats Serializer Class.
    """

    class Meta(object):
        model = VideoStats
        fields = [
            "view_count",
            "like_count",
            "favorite_count",
            "dislike_count",
            "comment_count"
        ]
        read_only_fields = (
            "created_at",
            "updated_at",
        )


class YoutubeVideosSerializer(TaggitSerializer, serializers.ModelSerializer):
    """
    Youtube Videos Serializer Class.
    """

    stats = VideoStatsSerializer(source="videostats", read_only=True)
    tags = TagListSerializerField()

    class Meta(object):
        model = YoutubeVideos
        fields = [
            "id",
            "channel_title",
            "channel_id",
            "video_id",
            "title",
            "description",
            "thumbnails_default_url",
            "thumbnails_default_width",
            "thumbnails_default_height",
            "duration",
            "published_at",
            "stats",
            "tags"
        ]
        read_only_fields = (
            "created_at",
            "updated_at",
            "channel_id"
        )
