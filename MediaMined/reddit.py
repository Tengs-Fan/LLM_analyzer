import os
import praw
from .db import mongo

from dotenv import load_dotenv
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent='macos:research_get_comment:v0.1 (by u/Frind-Study)'
)

def get_top_posts(subreddit_name, limit=None):
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.top('all', limit=limit):  # 'all' for all-time top posts
        if submission.score > 100:  # Filter by upvotes
            try:
                get_post_and_comments(submission.url)
            except :
                print(f'Subreddit post not found: {submission.url}')

def get_post_and_comments(url, sort='all', limit=None):
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
    mongo.reddit_insert_post(post)

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
        mongo.reddit_insert_comment(comment_data)
