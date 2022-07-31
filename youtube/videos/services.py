from django.db import transaction
from youtube.models import VideoStats, YoutubeVideos
import logging

logger = logging.getLogger(__name__)

try:
    from youtube.videos.config import *
except ImportError:
    raise ImportError('Configuration file not configured properly.')


class YoutubeVideoService:
    """
    A service for fetching youtube videos.
    """

    def __init__(self):
        """
        Class constructor
        """
        self.channel_id = os.environ.get('CHANNEL_ID', None)

    def _get_channel_videos_ids(self):
        """
        Get channel videos ids.
        Returns:
            a channel videos list.
        """
        req = youtube.channels().list(
            id=self.channel_id,
            part='contentDetails'
        )
        result = req.execute()
        playlist_id = result['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        video_ids = []
        next_page_token = None
        while True:
            res = youtube.playlistItems().list(playlistId=playlist_id,
                                               part='snippet',
                                               maxResults=50,
                                               pageToken=next_page_token).execute()
            video_ids += res['items']
            next_page_token = res.get('nextPageToken')
            if next_page_token is None:
                break
        return video_ids

    def video_details(self):
        """
        Get videos details.
        Returns:
            a list for videos details
        """
        video_ids = list(map(lambda x: x['snippet']['resourceId']['videoId'], self._get_channel_videos_ids()))
        videos = []
        for i in range(0, len(video_ids), 50):
            res = youtube.videos().list(id=','.join(video_ids[i:i + 50]),
                                        part='snippet,contentDetails, statistics').execute()
            videos += res['items']
        return videos

    def _snippet(self):
        """
        Get video snippet & content details information.
        Returns:
            a list for snippet & content details information
        """
        videos = self.video_details()
        snippet_data = []
        for video in videos:
            if 'channelTitle' in video['snippet']:
                channel_title = video['snippet']['channelTitle']
            else:
                channel_title = None

            if 'channelId' in video['snippet']:
                channel_id = video['snippet']['channelId']
            else:
                channel_id = None

            if 'title' in video['snippet']:
                title = video['snippet']['title']
            else:
                title = None

            if 'description' in video['snippet']:
                description = video['snippet']['description']
            else:
                description = None

            if 'thumbnails' in video['snippet'] and 'default' in video['snippet']['thumbnails'] and 'url' in \
                    video['snippet']['thumbnails']['default']:
                url = video['snippet']['thumbnails']['default']['url']
            else:
                url = None

            if 'thumbnails' in video['snippet'] and 'default' in video['snippet']['thumbnails'] and 'width' in \
                    video['snippet']['thumbnails']['default']:
                width = video['snippet']['thumbnails']['default']['width']
            else:
                width = None

            if 'thumbnails' in video['snippet'] and 'default' in video['snippet']['thumbnails'] and 'height' in \
                    video['snippet']['thumbnails']['default']:
                height = video['snippet']['thumbnails']['default']['height']
            else:
                height = None

            if 'publishedAt' in video['snippet']:
                published_at = video['snippet']['publishedAt']
            else:
                published_at = None
            if 'duration' in video['contentDetails']:
                duration = video['contentDetails']['duration']
            else:
                duration = None
            video_tags = []
            if 'tags' in video['snippet']:
                for tag in video['snippet']['tags']:
                    video_tags.append({'tag_name': tag})
            content = {
                'channelTitle': channel_title,
                'channelId': channel_id,
                'video_id': video['id'],
                'title': title,
                'description': description,
                'url': url,
                'width': width,
                'height': height,
                'duration': duration,
                'publishedAt': published_at,
                'tags': video_tags
            }
            snippet_data.append(content)
        return snippet_data

    def _stats(self):
        """
        Get video statistics
        Returns:
            a list for video statistics.
        """
        videos = self.video_details()
        stats = []
        for video in videos:
            if 'viewCount' in video['statistics']:
                view_count = video['statistics']['viewCount']
            else:
                view_count = 0

            if 'likeCount' in video['statistics']:
                like_count = video['statistics']['likeCount']
            else:
                like_count = 0

            if 'favoriteCount' in video['statistics']:
                favorite_count = video['statistics']['favoriteCount']
            else:
                favorite_count = 0

            if 'commentCount' in video['statistics']:
                comment_count = video['statistics']['commentCount']
            else:
                comment_count = 0
            if 'dislikeCount' in video['statistics']:
                dislike_count = video['statistics']['dislikeCount']
            else:
                dislike_count = 0

            statistics = {
                'video_id': video['id'],
                'viewCount': view_count,
                'likeCount': like_count,
                'favoriteCount': favorite_count,
                'commentCount': comment_count,
                'dislikeCount': dislike_count

            }
            stats.append(statistics)
        return stats

    def save_video_db(self):
        """
        Save data to the database.
        Returns:

        """
        videos = self._snippet()
        stats = self._stats()
        bulk_list_video_stat = list()
        with transaction.atomic():
            for video, stat in zip(videos, stats):
                obj, created = YoutubeVideos.objects.get_or_create(
                    video_id=video['video_id'],
                    defaults={
                        'channel_title': video['channelTitle'],
                        'channel_id': video['channelId'],
                        'title': video['title'],
                        'description': video['description'],
                        'thumbnails_default_url': video['url'],
                        'thumbnails_default_width': video['width'],
                        'thumbnails_default_height': video['height'],
                        'duration': video['duration'],
                        'published_at': video['publishedAt']
                    }
                )
                if created:
                    bulk_list_video_stat.append(
                        VideoStats(
                            youtube_video_id=obj.id,
                            video_id=stat['video_id'],
                            view_count=stat['viewCount'],
                            like_count=stat['likeCount'],
                            favorite_count=stat['favoriteCount'],
                            dislike_count=stat['dislikeCount'],
                            comment_count=stat['commentCount']
                        )
                    )
                    for tag in video['tags']:
                        obj.tags.add(tag['tag_name'])
            VideoStats.objects.bulk_create(bulk_list_video_stat)

    def update_video_stats(self):
        """
        Update video stats
        Returns:

        """
        stats = self._stats()
        with transaction.atomic():
            for stat in stats:
                VideoStats.objects.filter(
                    video_id=stat['video_id']
                ).update(
                    view_count=stat['viewCount'],
                    like_count=stat['likeCount'],
                    favorite_count=stat['favoriteCount'],
                    dislike_count=stat['dislikeCount'],
                    comment_count=stat['commentCount']
                )
