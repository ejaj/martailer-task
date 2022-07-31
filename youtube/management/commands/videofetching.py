from django.core.management.base import BaseCommand
from youtube.videos.services import YoutubeVideoService
import os


class Command(BaseCommand):
    """
    Command for fetching videos from youtube.
    """
    help = 'Fetch videos from youtube'

    def handle(self, *args, **options):
        """
        Handle a command for fetching videos.
        Args:
            *args:
            **options:

        Returns:

        """
        self.stdout.write(self.style.SUCCESS('Initialization has started.....'))
        service = YoutubeVideoService()
        service.save_video_db()
        self.stdout.write(self.style.SUCCESS('Video created or updated successfully.....'))
