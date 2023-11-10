from pymongo import MongoClient

client = MongoClient('localhost', 27017)
reddit = client['reddit']
youtube = client['youtube']

def get_items_by_id(collection, key, id):
    """
    Searches for and returns all comments belonging to a specific post_id.

    :param collection: The collection to search
    :param key: The key to search in the collection
    :param id:  The ID of the submission to search comments for.
    :return: A cursor to iterate over the comments belonging to the specified submission.
    """
    cursor = collection.find({key: id})
    items_list = list(cursor)
    if len(items_list) > 1:
        return items_list
    elif items_list:
        return items_list[0]
    else:
        raise Exception(f"can't find this {id} of {key} in {collection}")

def test_exist_in_collection(collection, key, id):
    """
    :return: If the id exist in collection, True; not exist, False
    """
    return collection.count_documents({ key: id }, limit = 1) != 0

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

def youtube_exist_dictation(video_id):
    return youtube_dictation.count_documents({ '_id': video_id }, limit = 1) != 0

def youtube_get_dictation_by_video_id(video_id):
    return youtube_dictation.find_one({"_id": video_id})

def youtube_exist_comment(comment_id):
    return youtube_comments.count_documents({ '_id': comment_id }, limit = 1) != 0

def youtube_get_comment_by_video_id(video_id):
    return get_items_by_id(youtube_comments, 'video_id', video_id);

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

def reddit_exist_post(post_id):
    return test_exist_in_collection(reddit_posts, '_id', post_id)

def reddit_get_post(post_id):
     return reddit_posts.find_one({"_id": post_id})

def reddit_exist_comment(comment_id):
    return test_exist_in_collection(reddit_comments, '_id', comment_id)

def reddit_insert_comment(document):
    try:
        reddit_comments.insert_one(document)
    except Exception as e:
        print(f"Could not store comment in MongoDB. Error: {e}")

def reddit_get_comment_by_id(comment_id):
    comment = reddit_comments.find_one({'_id': comment_id})
    return comment

def reddit_get_comments_by_post_id(post_id):
    return get_items_by_id(reddit_comments, 'post_id', post_id)

def reddit_get_top_comments_by_parent_id(parent_id, top_n = 50):
    comments_cursor = reddit_comments.find({'parent_id': parent_id}).sort('upvotes', -1).limit(top_n)
    comments_list = list(comments_cursor)
    raise Exception("NYI")
    return comments_list

def reddit_get_top_comments_by_post_id(post_id, top_n = 50):
    comments_cursor = reddit_comments.find({'post_id': "t3_" + post_id}).sort('upvotes', -1).limit(top_n)
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

