from .db import mongo
from .utils import utils

#######################################
# Composing Reddit posts
#######################################
def compose_reddit_post(post_collection, comment_collection, key, post_id):
    post = mongo._get_items_by_id(post_collection, key, post_id)
    if not post:
        raise Exception(f"Can't find {post_id}")

    if len(post) > 1 :
        print(f"post: {post[0]['id']} has more than 1 records in database, take the 1st one");

    composed_text = format_post_body(post[0])

    # Fetch the top comments for the post
    top_comments = mongo._get_top_from_key_and_sort(comment_collection, "parent_id", "t3_" + post_id, "score", 30);

    # Append the top comments to the composed text
    for comment in top_comments:
        composed_text += format_reddit_comments(comment)

    return composed_text

def format_post_body(post):

    # Check if 'ups' and 'downs' are available
    if 'ups' in post and 'downs' in post:
        upvotes = f"Upvotes: {post['ups']}"
        downvotes = f"Downvotes: {post['downs']}"
    else:
        upvotes = f"Score: {post['score']} (exact upvotes/downvotes not available)"
        downvotes = "\n"

    # Format the post details
    return f'''
{utils.utc_to_short_format(int(post['created_utc']))}
Subreddit: {post['subreddit']}
Author: {post['author']}
{upvotes} {downvotes}
Title: {post['title']}

{post['selftext']}
Comments:
---
'''


def format_reddit_comments(comment):
    # Format the comment details
    return f'''
{utils.utc_to_short_format(int(comment['created_utc']))}
By {comment['author']}
Upvotes: {comment['score']} 

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



