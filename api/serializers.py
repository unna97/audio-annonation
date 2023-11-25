# api/serializers.py
from rest_framework import serializers
from waveform_audio.models import AudioFile

class AudioFileSerializer(serializers.HyperlinkedModelSerializer):
  
    class Meta:
        model = AudioFile
        fields = ('id', 'file', 'timestamp')

