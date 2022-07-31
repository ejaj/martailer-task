from youtube.videos.services import YoutubeVideoService


def update_video_stats_scheduled_job():
    """

    Returns:

    """
    service = YoutubeVideoService()
    service.update_video_stats()
    print("Statistics updated")
