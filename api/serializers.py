# api/serializers.py
from rest_framework import serializers
from waveform_audio.models import AudioAnnotation

class AudioAnnotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AudioAnnotation
        fields = ('id', 'audio_file', 'annotation', 'start_time', 'end_time', 'timestamp')
