import os
from apiclient import discovery

import logging

logger = logging.getLogger(__name__)

api_key = os.environ.get('YOUTUBE_API_KEY', None)
if api_key:
    youtube = discovery.build('youtube', 'v3', developerKey=api_key)
else:
    logger.info("Youtube API key not found.")
