from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from db import sql
import os

# Set Up the API Client:
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=youtube_api_key)# 

def search_videos(youtube, query, max_results = 20):
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id,snippet",
        maxResults=max_results
    ).execute()

    return search_response['items']

def get_comments(video_id):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        order="relevance",
        maxResults=100
    )
    response = request.execute()
    for item in response["items"]:
        comment = process_comment_item(item)
        sql.insert_comment_data(comment)

def process_comment_item(item):
    snippet = item['snippet']
    top_level_comment = snippet['topLevelComment']['snippet']
    author_channel = top_level_comment['authorChannelId']

    # Prepare a dictionary with the relevant data
    comment_data = {
        'comment_id': item['id'],
        'video_id': snippet['videoId'],
        'channel_id': snippet['channelId'],
        'comment_text': top_level_comment['textOriginal'],
        'author_display_name': top_level_comment['authorDisplayName'],
        'author_profile_image_url': top_level_comment['authorProfileImageUrl'],
        'author_channel_url': top_level_comment['authorChannelUrl'],
        'author_channel_id': author_channel['value'] if author_channel else None,
        'like_count': top_level_comment['likeCount'],
        'published_at': top_level_comment['publishedAt'],
        'updated_at': top_level_comment['updatedAt'],
        'can_reply': snippet['canReply'],
        'total_reply_count': snippet['totalReplyCount'],
        'is_public': snippet['isPublic']
    }

    return comment_data

# Replace 'VIDEO_ID' with the ID of the YouTube video you're interested in
get_comments('094y1Z2wpJg')

# Example Usage:
# search_query = "Python programming tutorial"
# search_query = "Hong Kong"
# videos = search_videos(youtube, search_query)
# 1. download related video
# 2. get their text content
# 3. Platform, Original content, Summarized Content (1K Words), Subscribers, Channel Name, 
# 4. Comment Content, Thumb ups, Commenter Name, Discussions, Discussion Names, Discussion Thumb ups


