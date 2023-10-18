from pytube import YouTube
from utils import utils
from db import mongo
import os
import openai
from google.cloud import translate

# Constants
AUDIO_DIR = "Youtube"
openai.api_key = os.getenv("OPENAI_API_KEY")

def translate_to_english():
    client = translate.TranslationServiceClient()

def audio2text(audio_filepath):
    try:
        with open(audio_filepath, "rb") as audio_file:
            transcript = openai.Audio.translate("whisper-1", audio_file)
        return transcript
    except Exception as e:
        print(f"Failed to transcribe audio: {e}")
        return None

def download_audio(yt, video_id):
    audio_filename = f"{video_id}.mp3"
    audio_filepath = os.path.join(AUDIO_DIR, audio_filename)

    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=AUDIO_DIR, filename=audio_filename)
    print(f"Audio downloaded for {video_id}")

    return audio_filepath

def get_any_caption(youtube):
    caption = youtube.captions.get_by_language_code('en')  # Assuming English captions
    if caption:
        caption_text = caption.generate_srt_captions()
    else:
        captions = youtube.captions.all()
        caption = captions[0]                              # Just have a caption 
        caption_text = caption.generate_srt_captions()

    return caption_text


def video2text(video_url):
    video_id = utils.get_id_from_url(video_url)

    if mongo.find_in_video_text(video_id):
        print(f"Transcript for {video_id} already exists in database.")
        return None

    yt = YouTube(video_url)

    # Attempt to get captions
    caption = get_any_caption(yt)
    if caption:
        document = {"_id": video_id, "text": caption}
        mongo.insert2video_text(document)
    else:
        # If no captions, download audio
        audio_filepath = download_audio(yt, video_id)
        transcript = audio2text(audio_filepath)
        if transcript:
            document = {"_id": video_id, "text": transcript}
            mongo.insert2video_text(document)

# video2text("https://www.youtube.com/watch?v=CynzeRes7mY")
