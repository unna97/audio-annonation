from django.db import models
from .utils import file_hash
from django.core.exceptions import ValidationError
import datetime as dt
from datetime import time
from django.utils.translation import gettext_lazy as _
from django.core import checks


# Abstract model classes:
class TimeBoundLabelAbstract(models.Model):

    id = models.AutoField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    audio_file = models.ForeignKey("AudioFile", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = None  # This will be set by the subclass

    class Meta:
        abstract = True
        ordering = ["start_time", "end_time"]

    @staticmethod
    def parse_time(time_value):
        if isinstance(time_value, time):
            return time_value
        if isinstance(time_value, dt.timedelta):
            time_value = str(time_value)
            # check if the time value is in the format HH:MM:SS.%f, if not, add the missing parts with 0:
            if "." not in time_value:
                time_value += ".0"

        if isinstance(time_value, str):
            try:
                return dt.datetime.strptime(time_value, "%H:%M:%S.%f").time()
            except ValueError:
                try:
                    return dt.time.fromisoformat(time_value)
                except ValueError:
                    raise ValidationError(
                        f"Invalid time format: {time_value}. Use HH:MM:SS.%f or ISO format or time delta."
                    )
        raise ValidationError(
            f"Invalid time type: {type(time_value)}. Use string or time object."
        )

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError(_("End time must be after start time."))

    def duration(self):
        start_datetime = dt.datetime.combine(dt.datetime.min, self.start_time)
        end_datetime = dt.datetime.combine(dt.datetime.min, self.end_time)
        return end_datetime - start_datetime

    def save(self, *args, **kwargs):
        self.start_time = self.parse_time(self.start_time)
        self.end_time = self.parse_time(self.end_time)
        self.full_clean()
        super().save(*args, **kwargs)

    @classmethod
    def check(cls, **kwargs):
        errors = super().check(**kwargs)
        if not any(f.name == "content" for f in cls._meta.fields):
            errors.append(
                checks.Error(
                    f"Subclasses of {cls.__name__} must define 'content' field",
                    hint="Add a 'content' field to your model.",
                    obj=cls,
                    id="models.E001",
                )
            )
        return errors


# Models:
class AudioFile(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="audio/", unique=True)
    file_hash = models.CharField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # TODO: Add audio file details model

    def __str__(self):
        return str(self.file)

    def save(self, *args, **kwargs):
        if not self.pk:  # Only on creation
            self.file_hash = file_hash(self.file)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["timestamp"]
        db_table = "audio_file"
        verbose_name = "Audio File"
        verbose_name_plural = "Audio Files"


class AudioAnnotation(TimeBoundLabelAbstract):

    content = models.CharField(
        max_length=255, help_text=_("Annotation label of the audio segment")
    )

    class Meta(TimeBoundLabelAbstract.Meta):
        db_table = "audio_annotation"
        # TODO: Add a Annotator model and field
        # make sure the annotation is unique:
        unique_together = ["audio_file", "start_time", "end_time", "content"]
        verbose_name = "Audio Annotation"
        verbose_name_plural = "Audio Annotations"

    def __str__(self):
        return (
            f"{self.audio_file} - {self.content} ({self.start_time} to {self.end_time})"
        )


class Subtitle(TimeBoundLabelAbstract):

    content = models.TextField(help_text=_("Subtitle content"))
    # language = models.CharField(max_length=255, default="en")
    class Meta(TimeBoundLabelAbstract.Meta):
        db_table = "subtitle"
        # make sure the subtitle is unique:
        unique_together = ["audio_file", "start_time", "end_time"]
        verbose_name = "Subtitle"
        verbose_name_plural = "Subtitles"
