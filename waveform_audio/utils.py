import srt
from typing import Dict, List, Any


def process_subtitle_file(subtitle_file) -> List[Dict[str, Any]]:
    # read the subtitle file
    subtitle_text = subtitle_file.read().decode("utf-8")

    subtitle_generator = srt.parse(subtitle_text)
    # convert the subtitle generator to a list of subtitle dictionaries:
    subtitles_list = [
        {
            "content": subtitle.content,
            "start_time": subtitle.start,
            "end_time": subtitle.end,
        }
        for subtitle in subtitle_generator
    ]

    return subtitles_list
