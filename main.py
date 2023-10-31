from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from logging import getLogger
from MediaMined.db import mongo 
import MediaMined.reddit as reddit

main = Blueprint('main', __name__)
logger = getLogger(__name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/reddit')
@login_required
def reddits():
    total_posts = mongo.get_total_posts_count()
    posts = mongo.get_all_posts()
    average_upvotes = 0.7
    return render_template('reddit.html', posts=posts, total_posts=total_posts, average_upvotes = average_upvotes)

@main.route('/reddit/<post_id>')
@login_required
def reddit_post(post_id):
    logger.info("access reddit posts")
    # Fetch the post details from the database
    post = mongo.find_post(post_id)
    # Fetch the comments associated with this post
    comments = mongo.find_comments_by_post(post_id)
    return render_template('reddit_post.html', post=post, comments=comments)

@main.route('/submit_reddit_url', methods=['POST'])
@login_required
def submit_reddit_url():
    url = request.form['url']

    reddit.get_content(url);
    
    return redirect(url_for('main.reddits'))  # Redirect back to the index page

# @main.route('/youtube')
# @login_required
# def youtubes():
#     # total_videos = mongo.get_total_videos_count()
#     # videos = mongo.get_all_videos()
#     # average_likes = 0.9  # Example, adjust as needed
#     return render_template('youtube.html', videos=videos, total_videos=total_videos, average_likes=average_likes)

# @main.route('/youtube/<video_id>')
# @login_required
# def youtube_video(video_id):
#     logger.info("access YouTube video")
#     video = mongo.find_video(video_id)
#     comments = mongo.find_comments_by_video(video_id)
#     return render_template('youtube_video.html', video=video, comments=comments)
