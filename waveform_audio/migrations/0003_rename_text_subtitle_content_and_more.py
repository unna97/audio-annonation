# Generated by Django 5.0 on 2024-07-13 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("waveform_audio", "0002_subtitle"),
    ]

    operations = [
        migrations.RenameField(
            model_name="subtitle",
            old_name="text",
            new_name="content",
        ),
        migrations.AlterUniqueTogether(
            name="audiofile",
            unique_together={("file",)},
        ),
        migrations.AlterUniqueTogether(
            name="subtitle",
            unique_together={("audio_file", "start_time", "end_time")},
        ),
    ]
