from django.db import models


class AudioFile(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="audio/")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.file)

    class Meta:
        ordering = ["timestamp"]
        db_table = "audio_file"
        # make sure the file is unique:
        unique_together = ["file"]


class AudioAnnotation(models.Model):
    class AnnotationLabel(models.TextChoices):
        SPEECH = "speech"
        MUSIC = "music"
        NOISE = "noise"
        LAUGHTER = "laughter"
        OTHER = "other"
        UNKNOWN = "unknown"

    id = models.AutoField(primary_key=True)
    audio_file = models.ForeignKey(
        AudioFile, on_delete=models.CASCADE, related_name="annotations"
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    annotation = models.CharField(
        max_length=10, choices=AnnotationLabel.choices, default=AnnotationLabel.UNKNOWN
    )
    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time", "end_time"]
        db_table = "audio_annotation"


class Subtitle(models.Model):

    id = models.AutoField(primary_key=True)
    audio_file = models.ForeignKey(
        AudioFile, on_delete=models.CASCADE, related_name="subtitles"
    )
    start_time = models.DurationField()
    end_time = models.DurationField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["start_time", "end_time"]
        db_table = "subtitle"
        # make sure the subtitle is unique:
        unique_together = ["audio_file", "start_time", "end_time"]
