# api/serializers.py
# from calendar import c
from rest_framework import serializers
from waveform_audio.models import AudioFile, AudioAnnotation


class AudioFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AudioFile
        fields = ("id", "file", "timestamp")


# fetch AudioAnnotations from database based on audio file:
class AudioAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioAnnotation
        fields = (
            "id",
            "audio_file",
            "start_time",
            "end_time",
            "content",
            "timestamp",
        )

    def create(self, validated_data):
        return AudioAnnotation.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.start_time = validated_data.get("start_time", instance.start_time)
        instance.end_time = validated_data.get("end_time", instance.end_time)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance
