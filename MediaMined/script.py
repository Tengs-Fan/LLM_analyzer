from .llm import * 
from .youtube import *
from .reddit import *
from .db import mongo

# script to directly run in CLI

def update_videos():
    for video in mongo.youtube_get_all_dictations():
        video_id = video['_id']
        stat = get_stat(video_id)
        mongo.youtube_update_dictation(video_id, stat)

# update_videos()
# summarize_video_dictation("test", 10)

def youtube():
    # search_and_get("HongKong Resistance", 5000)
    search_and_get("HongKong Protest", 5000)
    search_and_get("HongKong Security", 5000)
    search_and_get("香港 抗議", 5000)
    search_and_get("香港 國安法", 5000)

def reddit():
    # get_top_posts("HongKong")
    # get_top_posts("HongKongProtest")
    # get_top_posts("Cantonese")
    get_top_posts("LIHKG")
    get_top_posts("Hong_Kong")
    get_top_posts("HKGLounge")

if __name__ == "__main__":
    import sys

    # Check if a specific function name is passed as a command line argument
    if sys.argv[1] == "youtube":
        youtube()
    elif sys.argv[1] == "reddit":
        reddit()
