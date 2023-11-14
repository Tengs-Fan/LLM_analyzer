from .db import mongo
from .utils import utils

#######################################
# Composing Reddit posts
#######################################
def compose_reddit_post(post_id):
    post = mongo.reddit_get_post(post_id)
    if not post:
        raise Exception("Can't find {post_id}")

    composed_text = format_post_body(post)
    
    # Fetch the top comments for the post
    top_comments = mongo.reddit_get_top_comments_by_post_id(post_id)

    # Append the top comments to the composed text
    for comment in top_comments:
        composed_text += format_reddit_comments(comment)

    return composed_text

def format_post_body(post):
    # Format the post details including author, date, upvotes, etc.
    return f'''
{utils.iso8601_to_short_format(post['published_at'])}
Upvotes: {post['upvotes']}
Title: {post['title']}

{post['content']}
Comments:
---'''


def format_reddit_comments(comment):
    # Format the comment details
    return f'''
{utils.iso8601_to_short_format(comment['published_at'])}
By {comment['author']}
Upvotes: {comment['upvotes']} 

{comment['body']}
---'''


#######################################
# Composing Youtube Video
#######################################
def compose_youtube_video(video_id):
    video_dictation = mongo.youtube_get_dictation_by_video_id(video_id)
    if not video_dictation:
        raise Exception(f"Can't find dictation for video {video_id}")

    composed_text = format_video_dictation(video_dictation)
    
    # Fetch the top comments for the video
    top_comments = mongo.youtube_get_comment_by_video_id(video_id)

    # Append the top comments to the composed text
    for comment in top_comments:
        composed_text += format_youtube_comments(comment)

    return composed_text

def format_video_dictation(video_dictation):
    # Format the video details including title, view count, etc.
    # Assuming you have a 'title' and 'viewCount' in your video_dictation object
    return f'''
Dictation {video_dictation['text']}
Comments:
---'''
# {utils.iso8601_to_short_format(video_dictation['published_at'])}
# Views: {video_dictation['viewCount']}
# Title: {video_dictation['title']}
# Dictation: 
# {video_dictation['transcript']}

def format_youtube_comments(comment):
    # Format the comment details
    return f'''
{utils.iso8601_to_short_format(comment['published_at'])}
By {comment['author_display_name']}
Likes: {comment['like_count']} 
    {comment['comment_text']}
---'''



