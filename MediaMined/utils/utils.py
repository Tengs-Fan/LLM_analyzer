import re

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

def construct_youtube_url(video_id):
    base_url = "https://www.youtube.com/watch?v="
    return f"{base_url}{video_id}"

def construct_reddit_url_from_permalink(submission_permalink):
    # Regular expression pattern for a valid Reddit permalink
    pattern = r'^/r/\w+/comments/\w+/.+/?$'
    
    # Check if the permalink is valid
    if re.match(pattern, submission_permalink):
        # If valid, construct the full URL
        base_url = 'https://www.reddit.com'
        full_url = f"{base_url}{submission_permalink}"
        return full_url
    else:
        # If not valid, return a message or raise an exception
        raise ValueError("Not a valid permalink for reddit")
    
from datetime import datetime
def format_utc_to_iso8601(utc_timestamp):
    """
    Converts a UTC timestamp to a ISO8601 string (used by Youtube).

    :param utc_timestamp: The UTC timestamp as a float or int.
    :return: The ISO8601 string representation of the timestamp.
    """
    # Convert the timestamp to a datetime object
    utc_datetime = datetime.utcfromtimestamp(utc_timestamp)
    
    # Format the datetime object as a string
    iso8601_formatted_string = utc_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
    return iso8601_formatted_string

def iso8601_to_short_format(iso8601_string):
    # Parse the ISO 8601 formatted string into a datetime object
    datetime_obj = datetime.strptime(iso8601_string, "%Y-%m-%dT%H:%M:%SZ")
    # Format the datetime object into the specified custom format
    custom_format_string = datetime_obj.strftime("%Y %b %d %H:%M")
    return custom_format_string

def format_dict(d, indent=0):
    for key, value in d.items():
        print(' ' * indent + str(key) + ':', end='')
        if isinstance(value, dict):
            print()
            format_dict(value, indent + 4)
        else:
            print(f' {value}')

import tiktoken
def count_tokens(prompt):
    encoding = tiktoken.get_encoding("cl100k_base")
    num_tokens = len(encoding.encode(prompt))
    return num_tokens

