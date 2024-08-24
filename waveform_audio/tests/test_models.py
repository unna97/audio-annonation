from turtle import st
import pytest
from waveform_audio.models import AudioAnnotation, AudioFile
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
import os
import datetime as dt
import random


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
    def test_all_annotations_representations(
        self, audio_file_1, example_annotations, stored_example_annotations
    ):
        audio = AudioFile.objects.get_or_create(file=audio_file_1)[0]
        annotations = [
            AudioAnnotation.objects.create(
                audio_file=audio,
                start_time=example_annotations[i]["start_time"],
                end_time=example_annotations[i]["end_time"],
                content=example_annotations[i]["content"],
            )
            for i in range(len(example_annotations))
        ]
        for i, annotation in enumerate(annotations):
            assert (
                annotation.start_time == stored_example_annotations[i]["start_time"]
            ), f"Annotation {i} start time {annotation.start_time} should be {stored_example_annotations[i]['start_time']}"
            assert (
                annotation.end_time == stored_example_annotations[i]["end_time"]
            ), f"Annotation {i} end time {annotation.end_time} should be {stored_example_annotations[i]['end_time']}"
            assert (
                annotation.content == stored_example_annotations[i]["content"]
            ), f"Annotation {i} content {annotation.content} should be {stored_example_annotations[i]['content']}"
            assert (
                annotation.audio_file == audio
            ), f"Annotation {i} audio file {annotation.audio_file} should be {audio}"
            assert (
                annotation.duration() == stored_example_annotations[i]["duration"]
            ), f"Annotation {i} duration {annotation.duration()} should be {stored_example_annotations[i]['duration']}"

    def test_clean_method_valid_times(self, audio_file_1, example_annotations):
        audio = AudioFile.objects.get_or_create(file=audio_file_1)[0]
        annotation = AudioAnnotation(
            audio_file=audio,
            start_time=example_annotations[1]["start_time"],
            end_time=example_annotations[1]["end_time"],
            content=example_annotations[1]["content"],
        )
        annotation.clean()  # Should not raise an exception

    def test_clean_method_invalid_times(self, audio_file_1, example_annotations):
        audio = AudioFile.objects.get_or_create(file=audio_file_1)[0]
        annotation = AudioAnnotation(
            audio_file=audio,
            start_time=example_annotations[2]["end_time"],
            end_time=example_annotations[2]["start_time"],
            content=example_annotations[2]["content"],
        )
        with pytest.raises(ValidationError):
            annotation.clean()

    def test_ordering(
        self, audio_file_1, example_annotations, stored_example_annotations
    ):
        audio = AudioFile.objects.get_or_create(file=audio_file_1)[0]
        # randomize the order of the annotations:
        example_annotations = random.sample(
            example_annotations, len(example_annotations)
        )
        annotation_inserted = [
            AudioAnnotation.objects.create(
                audio_file=audio,
                start_time=example_annotations[i]["start_time"],
                end_time=example_annotations[i]["end_time"],
                content=example_annotations[i]["content"],
            )
            for i in range(len(example_annotations))
        ]
        annotations = AudioAnnotation.objects.all()
        sorted_examples = sorted(
            stored_example_annotations, key=lambda x: (x["start_time"], x["end_time"])
        )

        for i, annotation in enumerate(annotations):
            assert (
                annotation.start_time == sorted_examples[i]["start_time"]
            ), f"Annotation {i} start time {annotation.start_time} should be {sorted_examples[i]['start_time']}"
            assert (
                annotation.end_time == sorted_examples[i]["end_time"]
            ), f"Annotation {i} end time {annotation.end_time} should be {sorted_examples[i]['end_time']}"
            assert (
                annotation.content == sorted_examples[i]["content"]
            ), f"Annotation {i} content {annotation.content} should be {sorted_examples[i]['content']}"
            assert (
                annotation.audio_file == audio
            ), f"Annotation {i} audio file {annotation.audio_file} should be {audio}"
            assert (
                annotation.duration() == sorted_examples[i]["duration"]
            ), f"Annotation {i} duration {annotation.duration()} should be {sorted_examples[i]['duration']}"

    def test_unique_together_constraint(self, audio_file_1, example_annotations):
        audio = AudioFile.objects.get_or_create(file=audio_file_1)[0]
        AudioAnnotation.objects.create(
            audio_file=audio,
            start_time=example_annotations[1]["start_time"],
            end_time=example_annotations[1]["end_time"],
            content=example_annotations[1]["content"],
        )
        with pytest.raises(ValidationError):
            AudioAnnotation.objects.create(
                audio_file=audio,
                start_time=example_annotations[1]["start_time"],
                end_time=example_annotations[1]["end_time"],
                content=example_annotations[1]["content"],
            )
