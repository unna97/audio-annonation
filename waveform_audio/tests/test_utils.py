import pytest
import datetime as dt
from waveform_audio.utils import process_subtitle_file


def test_process_subtitle_file(subtitles_file_1, subtitles_list_1):
    subtitles = process_subtitle_file(subtitles_file_1)
    assert len(subtitles) == 4
    for i in range(len(subtitles)):
        assert subtitles[i]["content"] == subtitles_list_1[i]["content"]
        assert subtitles[i]["start_time"] == subtitles_list_1[i]["start_time"]
        assert subtitles[i]["end_time"] == subtitles_list_1[i]["end_time"]
