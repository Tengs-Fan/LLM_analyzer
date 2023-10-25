import re
from datetime import datetime

def extract_id_from_url(url):
    """
    Extracts the Reddit post ID or YouTube video ID from a given URL.
    
    :param url: The Reddit post URL or YouTube video URL
    :return: The ID or None if not found
    """ 
    # For Reddit
    reddit_pattern = r"reddit\.com/r/[^/]+/comments/([^/]+)"
    reddit_match = re.search(reddit_pattern, url)
    
    if reddit_match:
        return reddit_match.group(1)
    
    # For YouTube
    youtube_pattern = r"youtube\.com/watch\?v=([a-zA-Z0-9_-]+)"
    youtube_match = re.search(youtube_pattern, url)
    
    if youtube_match:
        return youtube_match.group(1)

    raise ValueError("Unrecognizable URL")

def construct_reddit_url(submission_id):
    base_url = "https://redd.it/"
    reddit_url = f"{base_url}{submission_id}"
    return reddit_url

def format_utc_timestamp(utc_timestamp):
    """
    Converts a UTC timestamp to a human-readable string.

    :param utc_timestamp: The UTC timestamp as a float or int.
    :return: The human-readable string representation of the timestamp.
    """
    # Convert the timestamp to a datetime object
    dt_object = datetime.utcfromtimestamp(utc_timestamp)
    
    # Format the datetime object as a string
    human_readable_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')

    return human_readable_time

def format_dict(d, indent=0):
    for key, value in d.items():
        print(' ' * indent + str(key) + ':', end='')
        if isinstance(value, dict):
            print()
            format_dict(value, indent + 4)
        else:
            print(f' {value}')
