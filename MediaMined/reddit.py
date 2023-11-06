import os
import praw
import time     #sleep
from .utils import utils
from .db import mongo

from dotenv import load_dotenv
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv('REDDIT_CLIENT_ID'),
    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
    user_agent='macos:research_get_comment:v0.1 (by u/Frind-Study)',
    username=os.getenv('REDDIT_USER_NAME'),
    password=os.getenv('REDDIT_USER_PASSWORD')
)

def get_top_posts(subreddit_name, limit=None):
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.top('all', limit=limit):  # 'all' for all-time top posts
        # print(f"Going to get {submission} \t {submission.name}, {submission.title} at {submission.url} and {submission.permalink}")
        if submission.score > 50 and (not mongo.reddit_exist_post(submission.id)):  # Filter by upvotes
            time.sleep(1)
            try:
                url = utils.construct_reddit_url_from_permalink(submission.permalink)
                get_post_and_comments(url)
            except Exception as e:
                print("Met exception when trying to get post:", e)
                print(f'Subreddit post not found: {submission.url}, id: {submission.id}, permalink: {submission.permalink}')

def get_post_and_comments(url, comment_sort="top", limit=None):
    # Get the submission object for the given URL
    submission = reddit.submission(url=url)

    # print(f'Found post: {submission.title}')
    # print(f'Content: {submission.selftext}')  # This will be empty for link submissions
    post = {
        '_id': submission.id,
        'upvotes': submission.score,
        'upvote_ratio': submission.upvote_ratio,
        'title': submission.title,
        'content': submission.selftext,
        'published_at': utils.format_utc_to_iso8601(submission.created_utc),
        'num_comments': submission.num_comments,    
        'url': submission.url,
    }
    if (not mongo.reddit_exist_post(submission.id)):
        mongo.reddit_insert_post(post)
        print(f"Inserted post of {submission.id} to database, Now, I'm gonna fetch and insert the comments ");
        get_comments_from_submission(submission)
    else:
        print(f'Post {post["_id"]} at {post["url"]} already existed in database')


def get_comments_from_submission(submission, comment_sort="top", limit=None):

    submission.comment_sort = comment_sort
    while True:
        try:
            submission.comments.replace_more(limit=limit)
            break
        except Exception as e:
            print("Handling replace_more exception:", e)
            time.sleep(1)

    for comment in submission.comments.list():
        if comment.score > 5:   # ignore very low comment
            comment_data = {
                '_id': comment.id,
                'post_id': comment.submission.id,
                'author': str(comment.author),
                'body': comment.body,
                'upvotes': comment.score,
                'is_poster': comment.is_submitter,
                'post_id': comment.link_id,
                'parent_id': comment.parent_id,
                'published_at': utils.format_utc_to_iso8601(comment.created_utc),
                'replies_count': len(comment.replies)
            }
            if (not mongo.reddit_exist_comment(submission.id)):
                mongo.reddit_insert_comment(comment_data)
            else:
                print(f'Comment {comment_data["_id"]} at {comment_data["post_id"]} already existed in database')

    print(f"Inserted comments of {submission.id} to database");

get_top_posts("HongKong")
get_top_posts("HongKongProtest")
