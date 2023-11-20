from .serializers import *
from rest_framework import generics
from waveform_audio.models import AudioAnnotation,AudioFile
from rest_framework.response import Response
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

    def post(self, request):
        serializer = AudioAnnotationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
class AudioFileListAPIView(generics.ListCreateAPIView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer

class AudioFileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer