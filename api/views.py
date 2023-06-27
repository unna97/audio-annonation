from django.shortcuts import render
from .serializers import *
from rest_framework import generics
from waveform_audio.models import AudioAnnotation
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.views import APIView




class AudioAnnotationViewSet(APIView):
    
    def get(self, request):
        #filter by audio_file:
        audio_file = request.query_params.get('audio_file', None)
        if audio_file is not None:
            audio_annotations = AudioAnnotation.objects.filter(audio_file=audio_file)
        else:
            audio_annotations = AudioAnnotation.objects.all()
        
        serializer = AudioAnnotationSerializer(audio_annotations, many=True)

        return Response(serializer.data)

