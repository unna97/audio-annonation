from email.mime import audio
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from waveform_audio.models import AudioFile
from django.db.utils import IntegrityError
from django import setup


class AudioFileModelTest(TestCase):
    def setUp(self):
        self.audio_file = SimpleUploadedFile(
            "test_audio.wav", b"file_content", content_type="audio/wav"
        )

    def test_create_audio_file(self):
        audio = AudioFile.objects.create(file=self.audio_file)
        self.assertTrue(isinstance(audio, AudioFile))
        self.assertEqual(audio.__str__(), str(audio.file))

    def test_unique_together_constraint(self):
        AudioFile.objects.create(file=self.audio_file)
        with self.assertRaises(IntegrityError):
            AudioFile.objects.create(file=self.audio_file)

    def test_ordering(self):
        AudioFile.objects.create(file=self.audio_file)
        AudioFile.objects.create(
            file=SimpleUploadedFile(
                "test_audio_2.mp3", b"file_content", content_type="audio/mpeg"
            )
        )
        audio_files = AudioFile.objects.all()
        self.assertEqual(
            audio_files[0].timestamp, audio_files.earliest("timestamp").timestamp
        )

    def test_file_hash(self):
        audio = AudioFile.objects.create(file=self.audio_file)
        # check if file_hash is created:
        self.assertTrue(audio.file_hash)
