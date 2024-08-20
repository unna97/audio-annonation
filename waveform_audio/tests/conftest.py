import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.utils import override_settings
from django.conf import settings
import os
import shutil


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
