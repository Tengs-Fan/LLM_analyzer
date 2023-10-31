from googleapiclient.discovery import build
from .utils import utils
from .db import mongo
import openai       # Get Dictation

import os
from dotenv import load_dotenv
load_dotenv()

# Set Up the API Client:
youtube_api_key = os.getenv("YOUTUBE_API_KEY")
youtube = build("youtube", "v3", developerKey=youtube_api_key) #, credentials=credentials) 
openai.api_key = os.getenv("OPENAI_API_KEY")

# Store the audio files in "Youtube" subfolder
AUDIO_DIR = "Youtube"       

# Set Up the API Client:
# videos = search_videos(youtube, search_query)
# 1. download related video
# 2. get their text content
# 3. Platform, Original content, Summarized Content (1K Words), Subscribers, Channel Name, 
# 4. Comment Content, Thumb ups, Commenter Name, Discussions, Discussion Names, Discussion Thumb ups

def store_dictation_and_comments(url):
    get_dictation(url)
    video_id = utils.extract_id_from_url(url)
    # get_captions(youtube, video_id)
    # get_comments(video_id)

def search_videos(youtube, query, max_results = 20):
    search_response = youtube.search().list(
        q=query,
        type="video",
        part="id,snippet",
        maxResults=max_results
    ).execute()

    return search_response['items']

#################################################################################
#                       Caption
#################################################################################
def get_dictation(video_url):
    video_id = utils.extract_id_from_url(video_url)

    if mongo.youtube_get_dictation_by_video_id(video_id):
        print(f"Transcript for {video_id} already exists in database.")
        return None

    # Attempt to get captions
    # caption_id = find_captions(video_id)
    # if caption_id:
    #     document = {"_id": video_id, "text": get_caption(video_url)}
    #     mongo.youtube_insert_dictation(document)
    # else:

    # If no captions, download audio
    audio_filepath = download_audio(video_url)
    # Get dicatation from audio
    dicatation = audio2text(audio_filepath)
    if dicatation:
        document = {"_id": video_id, "text": dicatation}
        mongo.youtube_insert_dictation(document)
    else:
        raise Exception("Can't get diactation")

#################################################################################
#                       Caption
#################################################################################
def find_captions(video_id):
    caption_list = youtube.captions().list(
        part="snippet",
        videoId=video_id
    ).execute()
    
    english_caption_id = None
    any_caption_id = None
    
    for caption in caption_list['items']:
        if 'en' in caption['snippet']['language']:
            english_caption_id = caption['id']
            break
        if any_caption_id is None:
            any_caption_id = caption['id']

    return english_caption_id or any_caption_id

def get_caption(video_url):
    try:
        any_cap = get_any_caption(video_url)
        # if any_cap is None:
        #     raise Exception(f"No Any Caption for {video_url}")
    except Exception:
        raise Exception(f"Should have caption for {video_url}")

# import pysubs2

# def extract_text(subtitle_file_path, output_file_path):
#     subs = pysubs2.load(subtitle_file_path)
#     with open(output_file_path, 'w', encoding='utf-8') as file:
#         for line in subs:
#             file.write(f"{line.text}\n")


def get_any_caption(video_url):
    video_id = utils.extract_id_from_url(video_url)

    ydl_opts = {
        'skip_download': True,      # We just want the subtitle
        'writesubtitles': True,
        'subtitleslangs': ['all'],  # All
        'subtitlesformat': 'vvt',
        'outtmpl': f"{AUDIO_DIR}/{video_id}.%(ext)s",
    }

    import yt_dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

        file_path = f"{AUDIO_DIR}/{video_id}"
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # return content

# def get_any_caption(video_url):
#     from pytube import YouTube
#     yt = YouTube(
#         video_url,
#         use_oauth=True, allow_oauth_cache=True
#     )

#     try:
#         # Get an iterator over the dictionary's items
#         iter_caption = iter(yt.captions.values())
#         # Get the first item
#         any_caption = next(iter_caption)
#         return any_caption.generate_srt_captions()
#     except StopIteration:
#         print(f"There is no caption for {video_url}.")
#         return None

#################################################################################
#                       Audio
# download, get dictation of audio
#################################################################################
def download_audio(video_url):
    video_id = utils.extract_id_from_url(video_url)

    from pytube import YouTube
    yt = YouTube(
        video_url,
        use_oauth=True, allow_oauth_cache=True
    )
    audio_filename = f"{video_id}.mp3"
    audio_filepath = os.path.join(AUDIO_DIR, audio_filename)

    # Check if the audio file already exists
    if os.path.exists(audio_filepath):
        print(f"Audio for {video_id} already exists at {audio_filepath}")
        return audio_filepath

    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=AUDIO_DIR, filename=audio_filename)
    print(f"Audio downloaded for {video_id}")

    return audio_filepath

def audio2text(audio_filepath):
    try:
        with open(audio_filepath, "rb") as audio_file:
            transcript = openai.Audio.translate("whisper-1", audio_file)
        return transcript
    except Exception as e:
        print(f"Failed to transcribe audio: {e}")
        return None

#################################################################################
#   Comments
#################################################################################
def get_comments(video_id):
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        textFormat="plainText",
        order="relevance",
        maxResults=100
    )
    response = request.execute()
    for item in response["items"]:
        comment = process_comment_item(item)
        mongo.youtube_insert_comments(comment)

def process_comment_item(item):
    snippet = item['snippet']
    top_level_comment = snippet['topLevelComment']['snippet']
    author_channel = top_level_comment['authorChannelId']

    # Prepare a dictionary with the relevant data
    comment_data = {
        '_id': item['id'],
        'video_id': snippet['videoId'],
        'channel_id': snippet['channelId'],
        'comment_text': top_level_comment['textOriginal'],
        'author_display_name': top_level_comment['authorDisplayName'],
        'author_profile_image_url': top_level_comment['authorProfileImageUrl'],
        'author_channel_url': top_level_comment['authorChannelUrl'],
        'author_channel_id': author_channel['value'] if author_channel else None,
        'like_count': top_level_comment['likeCount'],
        'published_at': top_level_comment['publishedAt'],
        'updated_at': top_level_comment['updatedAt'],
        'can_reply': snippet['canReply'],
        'total_reply_count': snippet['totalReplyCount'],
        'is_public': snippet['isPublic']
    }

    return comment_data

# store_dictation_comments("https://www.youtube.com/watch?v=NQbTMQZViTM")
# store_dictation_comments("https://www.youtube.com/watch?v=6_RdnVtfZPY")
store_dictation_and_comments("https://www.youtube.com/watch?v=zbSypV2ixjE")

