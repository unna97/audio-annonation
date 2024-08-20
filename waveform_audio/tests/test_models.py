import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from waveform_audio.models import AudioAnnotation, AudioFile
from django.db.utils import IntegrityError
import os
import hashlib


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
        # expected_hash = hashlib.sha256(audio_file_1.read()).hexdigest()
        # audio_file_1.seek(0)  # Reset file pointer
        # assert audio.file_hash == expected_hash

    def test_file_ordering(self, audio_file_1, audio_file_2):
        audio1 = AudioFile.objects.create(file=audio_file_1)
        audio2 = AudioFile.objects.create(file=audio_file_2)
        assert audio1.timestamp < audio2.timestamp
        audio_files = AudioFile.objects.all()
        assert audio_files[0].timestamp == audio_files.earliest("timestamp").timestamp


@pytest.mark.django_db
class TestAudioAnnotationModel:
    def test_create_audio_annotation(self, audio_file_1):
        audio = AudioFile.objects.get_or_create(file=audio_file_1)
        annonation = AudioAnnotation.objects.create(
            audio_file=audio[0],
            start_time="00:00:00",
            end_time="00:00:01",
            annotation="speech",
        )
        assert isinstance(annonation, AudioAnnotation)
        assert annonation.annotation == "speech"
        assert annonation.start_time == "00:00:00"
        assert annonation.end_time == "00:00:01"
        assert annonation.audio_file == audio[0]

    def test_unique_together_constraint(self, audio_file_1):
        audio = AudioFile.objects.get_or_create(file=audio_file_1)
        AudioAnnotation.objects.create(
            audio_file=audio[0],
            start_time="00:00:00",
            end_time="00:00:01",
            annotation="speech",
        )
        with pytest.raises(IntegrityError):
            AudioAnnotation.objects.create(
                audio_file=audio[0],
                start_time="00:00:00",
                end_time="00:00:01",
                annotation="speech",
            )
