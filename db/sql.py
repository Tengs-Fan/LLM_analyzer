import sqlite3

conn = sqlite3.connect('youtube_comments.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS comments (
    video_id TEXT,
    comment_id TEXT,
    comment_text TEXT,
    author_display_name TEXT,
    like_count INTEGER,
    published_at TEXT,
    total_reply_count INTEGER,
    PRIMARY KEY (comment_id)
);
''')

conn.commit()

def insert_comment_data(comment):
    """
    Insert a comment's data into the database.

    :param comment_data: A dictionary containing the comment data.
    """
    data_tuple = (
        comment['video_id'],
        comment['comment_id'],
        comment['comment_text'],
        comment['author_display_name'],
        comment['like_count'],
        comment['published_at'],
        comment['total_reply_count']
    )

    # Insert the data into the database
    cursor.execute('''
    INSERT INTO comments (video_id, comment_id, comment_text, author_display_name, like_count, published_at, total_reply_count)
    VALUES (?, ?, ?, ?, ?, ?, ?);
    ''', data_tuple)

    conn.commit()
