import os
from db import mongo
import praw

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

# get_content('https://www.reddit.com/r/fpgagaming/comments/17a1ph8/any_interest_in_a_lowcost_open_source_fpga/')
# print(mongo.find_post('17a1ph8'))
comments = mongo.find_comments_by_post('17a1ph8')  #

# mongo.find_comment_by_id()
# Or just the top comments
# top_comments = get_comments('https://www.reddit.com/r/example/comments/abc123/example_thread/', sort='top', limit=10)
