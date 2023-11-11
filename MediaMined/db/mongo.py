from pymongo import MongoClient

client = MongoClient('localhost', 27017)
reddit = client['reddit']
youtube = client['youtube']

def _get_items_by_id(collection, key, id):
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

def _test_exist_in_collection(collection, key, id):
    """
    :return: If the id exist in collection, True; not exist, False
    """
    return collection.count_documents({ key: id }, limit = 1) != 0

def _update_document(collection, query_key, query_value, update_data):
    """
    Update documents in a MongoDB collection based on a query.

    :param collection: The MongoDB collection to update.
    :param query_key: The field key to query the documents.
    :param query_value: The value to match for the query_key in the documents.
    :param update_data: A dictionary containing the fields to update and their new values.
    """
    # Step 1: Retrieve all matching documents from MongoDB
    cursor = collection.find({query_key: query_value})

    if cursor is None:
        raise Exception(f"Can't find documents with {query_key} = {query_value} in {collection.name}")

    # Step 2: Update each matching document
    collection.update_many(
        {query_key: query_value},
        {'$set': update_data}
    )

def _get_all(collection):
    """
    Retrieves all documents from the given collection.

    :return: A corsor of documents.
    """
    return collection.find()

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

def youtube_update_dictation(id, data):
    return _update_document(youtube_dictation, '_id', id, data)

def youtube_exist_dictation(video_id):
    return youtube_dictation.count_documents({ '_id': video_id }, limit = 1) != 0

def youtube_get_dictation_by_video_id(video_id):
    return youtube_dictation.find_one({"_id": video_id})

def youtube_exist_comment(comment_id):
    return youtube_comments.count_documents({ '_id': comment_id }, limit = 1) != 0

def youtube_get_comment_by_video_id(video_id):
    return _get_items_by_id(youtube_comments, 'video_id', video_id);

def youtube_get_all_dictations():
    return _get_all(youtube_dictation)

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
    return _test_exist_in_collection(reddit_posts, '_id', post_id)

def reddit_get_post(post_id):
     return reddit_posts.find_one({"_id": post_id})

def reddit_exist_comment(comment_id):
    return _test_exist_in_collection(reddit_comments, '_id', comment_id)

def reddit_insert_comment(document):
    try:
        reddit_comments.insert_one(document)
    except Exception as e:
        print(f"Could not store comment in MongoDB. Error: {e}")

def reddit_get_comment_by_id(comment_id):
    comment = reddit_comments.find_one({'_id': comment_id})
    return comment

def reddit_get_comments_by_post_id(post_id):
    return _get_items_by_id(reddit_comments, 'post_id', post_id)

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
    return _get_all(reddit_posts)

def reddit_get_total_posts_count():
    return reddit_posts.count_documents({})
