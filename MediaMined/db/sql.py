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

# from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
# from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "sqlite:///youtube_comments.db"  # SQLite database URL
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(bind=engine)

# metadata = MetaData()

# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Comment(Base):
#     __tablename__ = "comments"
#     
#     video_id = Column(String, nullable=False)
#     comment_id = Column(String, primary_key=True)
#     comment_text = Column(String, nullable=False)
#     author_display_name = Column(String, nullable=True)
#     like_count = Column(Integer, nullable=True)
#     published_at = Column(String, nullable=False)
#     total_reply_count = Column(Integer, nullable=True)

# Base.metadata.create_all(engine)

# def insert_comment_data(comment):
#     """
#     Insert a comment's data into the database.

#     :param comment_data: A dictionary containing the comment data.
#     """
#     # Create a new comment instance
#     new_comment = Comment(
#         video_id=comment['video_id'],
#         comment_id=comment['comment_id'],
#         comment_text=comment['comment_text'],
#         author_display_name=comment['author_display_name'],
#         like_count=comment['like_count'],
#         published_at=comment['published_at'],
#         total_reply_count=comment['total_reply_count']
#     )

#     # Insert the data into the database
#     session = SessionLocal()
#     session.add(new_comment)
#     session.commit()
#     session.close()


