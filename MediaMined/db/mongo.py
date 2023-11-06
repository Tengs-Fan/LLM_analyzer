from pymongo import MongoClient

client = MongoClient('localhost', 27017)
reddit = client['reddit']
youtube = client['youtube']

#######################################
# Text transcript of Youtube Video
#######################################
youtube_dictation = youtube['video_texts']
youtube_comments = youtube['video_comments']

def youtube_insert_dictation(document):
    try:
        youtube_dictation.insert_one(document)
    except Exception as e:
        print(f"Could not store dication of video in MongoDB. Error: {e}")

def youtube_insert_comments(document):
    try:
        youtube_comments.insert_one(document)
    except Exception as e:
        print(f"Could not store comments of video in MongoDB. Error: {e}")

def youtube_get_dictation_by_video_id(video_id):
    return youtube_dictation.find_one({"_id": video_id})

def youtube_get_comment_by_video_id(video_id):
    comments_cursor = youtube_comments.find({'video_id': video_id})
    comments_list = list(comments_cursor)
    return comments_list

#######################################
# Reddit Comments
#######################################
reddit_posts = reddit['reddit_post']
reddit_comments = reddit['reddit_comments']

def reddit_insert_post(document):
    try:
        reddit_posts.insert_one(document)
    except Exception as e:
        print(f"Could not store post in MongoDB. Error: {e}")

def reddit_get_post(post_id):
     return reddit_posts.find_one({"_id": post_id})

def reddit_insert_comment(document):
    try:
        reddit_comments.insert_one(document)
    except Exception as e:
        print(f"Could not store comment in MongoDB. Error: {e}")

def reddit_get_comment_by_id(comment_id):
    """
    Searches for and returns a comment document based on the comment ID.

    :param comment_id: The ID of the comment to search for.
    :return: The comment document, or None if no comment with the given ID is found.
    """
    comment = reddit_comments.find_one({'_id': comment_id})
    return comment

def reddit_get_comments_by_post_id(post_id):
    """
    Searches for and returns all comments belonging to a specific post_id.

    :param post_id: The ID of the submission to search comments for.
    :return: A cursor to iterate over the comments belonging to the specified submission.
    """
    comments_cursor = reddit_comments.find({'post_id': post_id})
    comments_list = list(comments_cursor)
    return comments_list

def reddit_get_all_posts():
    """
    Retrieves all documents from the reddit_post collection.

    :return: A list of documents.
    """
    cursor = reddit_posts.find()
    return list(cursor)

def reddit_get_total_posts_count():
    return reddit_posts.count_documents({})
