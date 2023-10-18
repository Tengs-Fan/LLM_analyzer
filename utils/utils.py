import re

def get_id_from_url(url):
    video_id_match = re.search(r'v=([^&]+)', url)
    if video_id_match:
        return video_id_match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")

def format_dict(d, indent=0):
    for key, value in d.items():
        print(' ' * indent + str(key) + ':', end='')
        if isinstance(value, dict):
            print()
            format_dict(value, indent + 4)
        else:
            print(f' {value}')
