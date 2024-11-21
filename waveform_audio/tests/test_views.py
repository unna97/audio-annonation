import pytest
import json
from datetime import time
import os

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

from waveform_audio.models import AudioFile, AudioAnnotation, Subtitle
from waveform_audio.forms import AudioModelFileForm, SubtitleFileForm
from waveform_audio.tests.conftest import subtitles_file_1


@pytest.mark.django_db
class TestAudioFileAvailableView:
    def test_view_renders_correctly(self, client, audio_file_1):
        AudioFile.objects.create(file=audio_file_1)
        response = client.get(reverse("index"))
        assert response.status_code == 200
        assert "audio_files" in response.context
        assert len(response.context["audio_files"]) > 0

    def test_view_with_no_audio_files(self, client):
        response = client.get(reverse("index"))
        assert response.status_code == 200
        assert "audio_files" in response.context
        assert len(response.context["audio_files"]) == 0


@pytest.mark.django_db
class TestUploadAudioAndSubtitleView:
    def test_get_request(self, client):
        response = client.get(reverse("upload"))
        assert response.status_code == 200
        assert "audio_form" in response.context
        assert "subtitle_form" in response.context

    def test_post_valid_files(self, client, audio_file_1, subtitles_file_1):
        response = client.post(
            reverse("upload"),
            data={"file": audio_file_1, "subtitle_file": subtitles_file_1},
            format="multipart",
        )

        assert response.status_code == 200
        assert AudioFile.objects.exists()
        assert Subtitle.objects.exists()

    def test_post_duplicate_file(self, client, audio_file_1, subtitles_file_1):

        client.post(
            reverse("upload"),
            data={"file": audio_file_1, "subtitle_file": subtitles_file_1},
            format="multipart",
        )

        # Second upload of same file
        response = client.post(
            reverse("upload"),
            data={"file": audio_file_1, "subtitle_file": subtitles_file_1},
            format="multipart",
        )

        assert response.status_code == 200
        assert AudioFile.objects.count() == 1


@pytest.mark.django_db
class TestAnnotateAudioFileView:
    def test_render_annotation_page(self, client, audio_file_1):
        audio = AudioFile.objects.create(file=audio_file_1)

        response = client.post(reverse("annotate"), {"audio_file": audio.id})

        assert response.status_code == 200
        assert "audio_file" in response.context
        assert "labels" in response.context

    def test_annotate_audio_without_subtitles(self, client, audio_file_1):
        audio = AudioFile.objects.create(file=audio_file_1)

        response = client.post(reverse("annotate"), {"audio_file": audio.id})

        assert response.status_code == 200
        assert "subtitles" in response.context
        assert len(response.context["subtitles"]) == 0


@pytest.mark.django_db
class TestSaveAnnotationsView:
    def test_save_valid_annotations(self, client, audio_file_1):
        audio = AudioFile.objects.create(file=audio_file_1)

        annotation_data = {
            "annotation_table": json.dumps(
                [
                    {"start_time": 1.0, "end_time": 5.0, "label": "laugh"},
                    {"start_time": 10.0, "end_time": 15.0, "label": "crowd"},
                ]
            ),
            "audio_id": audio.id,
        }

        response = client.post(
            reverse("save_annotations"),
            json.dumps(annotation_data),
            content_type="application/json",
        )

        assert response.status_code == 200
        assert AudioAnnotation.objects.filter(audio_file=audio).count() == 2

    def test_save_annotations_invalid_audio(self, client):
        annotation_data = {
            "annotation_table": json.dumps(
                [{"start_time": 1.0, "end_time": 5.0, "label": "laugh"}]
            ),
            "audio_id": 9999,  # Non-existent ID
        }

        response = client.post(
            reverse("save_annotations"),
            json.dumps(annotation_data),
            content_type="application/json",
        )

        assert response.status_code == 404
