from .llm import * 
from .youtube import *
from .reddit import *
from .compose import *
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

# if __name__ == "__main__":
#     import sys

#     # Check if a specific function name is passed as a command line argument
#     if len(sys.argv) > 1:
#         if sys.argv[1] == "youtube":
#             youtube()
#         elif sys.argv[1] == "reddit":
#             reddit()
#     else:
        # search_videos("HongKong", "viewCount", max_results = 50)
try: 
    text = compose_reddit_post("dfdqf8")
    print(text)
except Exception as e:
    print("error composing {17a1ph8}:", e)

# try: 
#     text = compose_youtube_video("CynzeRes7mY")
#     print(text)
# except Exception as e:
#     print(f"Error composing for video :", e)

