from .llm import * 
from .youtube import *
from .db import mongo
# script to directly run in CLI

# summarize_video_dictation("test", 10)
get_stat("B2NkjV-hSwk")

def update_videos():
    for video in mongo.youtube_get_all_dictations():
        video_id = video['_id']
        stat = get_stat(video_id)
        mongo.youtube_update_dictation(video_id, stat)

update_videos()


