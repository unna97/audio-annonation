import pytest
from waveform_audio.models import AudioAnnotation, AudioFile
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
import os
import datetime as dt


@pytest.mark.django_db
class TestAudioFileModel:
    def test_create_audio_file(self, audio_file_1):
        audio = AudioFile.objects.create(file=audio_file_1)
        assert isinstance(audio, AudioFile)
        # assert audio.__str__() == os.path.basename(audio.file.name)
        assert audio.file.name.endswith(".wav")
        assert os.path.exists(audio.file.path)

    def test_unique_together_constraint(self, audio_file_1):
        AudioFile.objects.create(file=audio_file_1)
        with pytest.raises(IntegrityError):
            AudioFile.objects.create(file=audio_file_1)

    def test_file_hash(self, audio_file_1):
        audio = AudioFile.objects.create(file=audio_file_1)
        assert audio.file_hash
        # TODO: test the hash value

    def test_file_ordering(self, audio_file_1, audio_file_2):
        audio1 = AudioFile.objects.create(file=audio_file_1)
        audio2 = AudioFile.objects.create(file=audio_file_2)
        assert audio1.timestamp < audio2.timestamp
        audio_files = AudioFile.objects.all()
        assert audio_files[0].timestamp == audio_files.earliest("timestamp").timestamp


@pytest.mark.django_db
class TestAudioAnnotationModel:
    def test_str_representation(self, audio_file_1):
        audio = AudioFile.objects.get_or_create(file=audio_file_1)[0]
        annotation = AudioAnnotation.objects.create(
            audio_file=audio,
            start_time="00:00:00",
            end_time="00:00:01",
            content="speech",
        )
        expected_str = f"{audio} - speech (00:00:00 to 00:00:01)"
        assert str(annotation) == expected_str

    def test_clean_method_valid_times(self, audio_file_1):
        audio = AudioFile.objects.get_or_create(file=audio_file_1)[0]
        annotation = AudioAnnotation(
            audio_file=audio,
            start_time="00:00:00",
            end_time="00:00:01",
            content="speech",
        )
        annotation.clean()  # Should not raise an exception

    def test_clean_method_invalid_times(self, audio_file_1):
        audio = AudioFile.objects.get_or_create(file=audio_file_1)[0]
        annotation = AudioAnnotation(
            audio_file=audio,
            start_time="00:00:01",
            end_time="00:00:00",
            content="speech",
        )
        with pytest.raises(ValidationError):
            annotation.clean()

    def test_duration_method(self, audio_file_1):
        audio = AudioFile.objects.get_or_create(file=audio_file_1)[0]
        annotation = AudioAnnotation.objects.create(
            audio_file=audio,
            start_time="00:00:00",
            end_time="00:00:10",
            content="speech",
        )
        expected_duration = dt.timedelta(seconds=10)
        assert annotation.duration() == expected_duration

    def test_ordering(self, audio_file_1):
        audio = AudioFile.objects.get_or_create(file=audio_file_1)[0]
        annotation1 = AudioAnnotation.objects.create(
            audio_file=audio,
            start_time="00:00:15",
            end_time="00:00:20",
            content="speech",
        )
        annotation2 = AudioAnnotation.objects.create(
            audio_file=audio,
            start_time="00:00:10",
            end_time="00:00:12",
            content="music",
        )
        annotations = AudioAnnotation.objects.all()
        assert annotations[0] == annotation2
        assert annotations[1] == annotation1
