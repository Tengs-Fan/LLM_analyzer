import os
import praw
from MediaMined.db import mongo

from dotenv import load_dotenv
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent='macos:research_get_comment:v0.1 (by u/Frind-Study)'
)

def get_content(url, sort='all', limit=None):
    # Get the submission object for the given URL
    submission = reddit.submission(url=url)

    # Print the submission's title and content
    print(f'Title: {submission.title}')
    print(f'Content: {submission.selftext}')  # This will be empty for link submissions
    post = {
        '_id': submission.id,
        'upvotes': submission.score,
        'upvote_ratio': submission.upvote_ratio,
        'title': submission.title,
        'content': submission.selftext
    }
    mongo.insert_post(post)

    ############## Get Comments #######################

    if sort == 'top':
        submission.comment_sort = 'top'
    elif sort == 'new':
        submission.comment_sort = 'new'
    # Other sorts can be added as needed

    # Replace "more" comments with their full content, up to a certain limit
    submission.comments.replace_more(limit=limit)

    for comment in submission.comments.list():
        comment_data = {
            '_id': comment.id,
            'post_id': comment.submission.id,
            'author': str(comment.author),
            'body': comment.body,
            'upvotes': comment.score,
            'is_poster': comment.is_submitter,
            'created_utc': comment.created_utc,
            'replies_count': len(comment.replies)
        }
        mongo.insert_comment(comment_data)
