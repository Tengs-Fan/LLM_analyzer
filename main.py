from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from MediaMined.db import mongo 
import MediaMined.reddit as reddit

main = Blueprint('main', __name__)

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
    
    return redirect(url_for('reddits'))  # Redirect back to the index page
