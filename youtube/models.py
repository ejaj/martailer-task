from django.db import models
from taggit.managers import TaggableManager


# Create your models here.

class YoutubeVideos(models.Model):
    """
    Stores a single youtube video entry.
    """
    channel_title = models.CharField(max_length=100, null=True, blank=True)
    channel_id = models.CharField(max_length=100, null=True, blank=True)
    video_id = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    thumbnails_default_url = models.CharField(max_length=100, null=True, blank=True)
    thumbnails_default_width = models.IntegerField(null=True, blank=True)
    thumbnails_default_height = models.IntegerField(null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    class Meta:
        ordering = ['-published_at']
        db_table = 'youtube_videos'

    def __str__(self):
        return self.video_id


# Create your models here.

class VideoStats(models.Model):
    """
    Stores a single video stats entry.
    """
    youtube_video = models.OneToOneField(
        YoutubeVideos,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    video_id = models.CharField(max_length=100, unique=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    favorite_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']
        db_table = 'video_stats'

    def __str__(self):
        return self.video_id
