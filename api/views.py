from .serializers import *
from rest_framework import generics, status
from waveform_audio.models import AudioFile
from rest_framework.response import Response
import os



class AudioFileDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AudioFile.objects.all()
    serializer_class = AudioFileSerializer #use HyperlinkedModelSerializer to get url field
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Get the file path and handle file deletion
        file_path = instance.file.path
        try:
            # Check if the file exists before attempting to delete
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            # Log the error or handle it based on your application's requirements
            # In a production environment, consider logging errors to a file or a monitoring system
            pass

        # Perform the standard destroy operation to delete the record from the database
        self.perform_destroy(instance)

        # Respond with a success status
        return Response(status=status.HTTP_204_NO_CONTENT)

class AudioFileUploadAPIView(generics.CreateAPIView):
    serializer_class = AudioFileSerializer
    queryset = AudioFile.objects.all()

class AudioFileListAPIView(generics.ListAPIView):
    serializer_class = AudioFileSerializer
    queryset = AudioFile.objects.all()
