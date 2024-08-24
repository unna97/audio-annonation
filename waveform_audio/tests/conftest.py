import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.utils import override_settings
import os
import shutil
import datetime as dt


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        # Your database setup code here, if needed
        pass


@pytest.fixture(scope="session")
def temp_media_root(tmp_path_factory):
    media_root = tmp_path_factory.mktemp("media")
    with override_settings(MEDIA_ROOT=str(media_root)):
        yield media_root
    shutil.rmtree(str(media_root), ignore_errors=True)


@pytest.fixture(autouse=True)
def temp_media(temp_media_root, settings):
    settings.MEDIA_ROOT = str(temp_media_root)


def read_fixture_file(filename):
    fixture_path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(fixture_path, "rb") as f:
        return f.read()


@pytest.fixture
def audio_file_1():
    content = read_fixture_file("test_audio.wav")
    return SimpleUploadedFile(
        "test_audio.wav", content=content, content_type="audio/wav"
    )


@pytest.fixture
def audio_file_2():
    content = read_fixture_file("test_audio_2.mp3")
    return SimpleUploadedFile(
        "test_audio_2.mp3", content=content, content_type="audio/mpeg"
    )


@pytest.fixture
def subtitles_file_1():
    content = read_fixture_file("test_subtitles.srt")
    return SimpleUploadedFile(
        "test_subtitles.srt", content=content, content_type="text/plain"
    )


@pytest.fixture
def example_annotations():
    return [
        # String time format:
        {"start_time": "00:00:00.089", "end_time": "00:00:05.78", "content": "music"},
        {"start_time": "00:00:15", "end_time": "00:00:30", "content": "speech"},
        # ISO format:
        {
            "start_time": dt.time(0, 0, 5),
            "end_time": dt.time(0, 0, 10),
            "content": "speech",
        },
        {
            "start_time": dt.time(0, 0, 10, 100),
            "end_time": dt.time(0, 0, 15, 200),
            "content": "speech",
        },
        # Time delta format:
        {
            "start_time": dt.timedelta(seconds=10),
            "end_time": dt.timedelta(seconds=15),
            "content": "noise",
        },
        {
            "start_time": dt.timedelta(seconds=15, milliseconds=100),
            "end_time": dt.timedelta(seconds=20, milliseconds=200),
            "content": "noise",
        },
    ]


@pytest.fixture
def stored_example_annotations():
    return [
        # String time format:
        {
            "start_time": dt.time(0, 0, 0, 89000),
            "end_time": dt.time(0, 0, 5, 780000),
            "content": "music",
            "duration": dt.timedelta(seconds=5, microseconds=691000),
        },
        {
            "start_time": dt.time(0, 0, 15),
            "end_time": dt.time(0, 0, 30),
            "content": "speech",
            "duration": dt.timedelta(seconds=15),
        },
        # ISO format:
        {
            "start_time": dt.time(0, 0, 5),
            "end_time": dt.time(0, 0, 10),
            "content": "speech",
            "duration": dt.timedelta(seconds=5),
        },
        {
            "start_time": dt.time(0, 0, 10, 100),
            "end_time": dt.time(0, 0, 15, 200),
            "content": "speech",
            "duration": dt.timedelta(seconds=5, microseconds=100),
        },
        # Time delta format (converted to time format):
        {
            "start_time": dt.time(0, 0, 10),
            "end_time": dt.time(0, 0, 15),
            "content": "noise",
            "duration": dt.timedelta(seconds=5),
        },
        {
            "start_time": dt.time(0, 0, 15, 100000),
            "end_time": dt.time(0, 0, 20, 200000),
            "content": "noise",
            "duration": dt.timedelta(seconds=5, milliseconds=100),
        },
    ]


# TODO: Add a speech audio and corresponding srt
# @pytest.fixture
# def subtitles_file_2():
#     content = read_fixture_file("test_subtitles_2.srt")
#     return SimpleUploadedFile(
#         "test_subtitles_2.srt", content=content, content_type="text/plain"
#     )
