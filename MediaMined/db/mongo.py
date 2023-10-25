from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
reddit = client['reddit']
youtube = client['database']

#######################################
# Text transcript of Youtube Video
#######################################
video_texts = youtube['video_texts']

def insert2video_text(document):
    try:
        video_texts.insert_one(document)
    except Exception as e:
        print(f"Could not store transcript in MongoDB. Error: {e}")

def find_in_video_text(video_id):
     return video_texts.find_one({"_id": video_id})

def get_from_id(video_id):
    document = video_texts.find_one({'_id': video_id})
    return document

#######################################
# Reddit Comments
#######################################
reddit_posts = reddit['reddit_post']
reddit_comments = reddit['reddit_comments']

def insert_post(document):
    try:
        reddit_posts.insert_one(document)
    except Exception as e:
        print(f"Could not store post in MongoDB. Error: {e}")

def find_post(post_id):
     return reddit_posts.find_one({"_id": post_id})

def insert_comment(document):
    try:
        reddit_comments.insert_one(document)
    except Exception as e:
        print(f"Could not store comment in MongoDB. Error: {e}")

def find_comment_by_id(comment_id):
    """
    Searches for and returns a comment document based on the comment ID.

    :param comment_id: The ID of the comment to search for.
    :return: The comment document, or None if no comment with the given ID is found.
    """
    comment = reddit_comments.find_one({'_id': comment_id})
    return comment

def find_comments_by_post(post_id):
    """
    Searches for and returns all comments belonging to a specific post_id.

    :param post_id: The ID of the submission to search comments for.
    :return: A cursor to iterate over the comments belonging to the specified submission.
    """
    comments_cursor = reddit_comments.find({'post_id': post_id})
    comments_list = list(comments_cursor)
    return comments_list

def get_all_posts():
    """
    Retrieves all documents from the reddit_post collection.

    :return: A list of documents.
    """
    cursor = reddit_posts.find()
    return list(cursor)

def get_total_posts_count():
    return reddit_posts.count_documents({})
