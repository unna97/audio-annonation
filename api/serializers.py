# api/serializers.py
from rest_framework import serializers
from waveform_audio.models import AudioAnnotation, AudioFile

class AudioAnnotationSerializer(serializers.ModelSerializer):

    class Meta:
        model = AudioAnnotation
        fields = ('id', 'audio_file', 'annotation', 'start_time', 'end_time', 'timestamp')

    def create(self, validated_data):
        return AudioAnnotation.objects.create(**validated_data)

class AudioFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = AudioFile
        fields = ('id', 'file', 'timestamp')
    
    def create(self, validated_data):
        
        return AudioFile.objects.create(**validated_data)

    

    