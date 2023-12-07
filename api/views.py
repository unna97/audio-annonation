from .serializers import *
from rest_framework import generics, status
from waveform_audio.models import AudioFile, AudioAnnotation
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


    def options(self, request, *args, **kwargs):
        """
        Don't include the view description in OPTIONS responses.
        """
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)
        data.pop('description')
        return Response(data=data, status=status.HTTP_200_OK)        
        

class AudioFileUploadAPIView(generics.CreateAPIView):
    serializer_class = AudioFileSerializer
    queryset = AudioFile.objects.all()

class AudioFileListAPIView(generics.ListAPIView):
    serializer_class = AudioFileSerializer
    queryset = AudioFile.objects.all()


class AudioAnnotationListAPIView(generics.ListAPIView):
    serializer_class = AudioAnnotationSerializer
    queryset = AudioAnnotation.objects.all()
    lookup_field = "audio_file_id"

    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    

    def get_queryset(self):
        audio_file_id = self.kwargs['audio_file_id']
        return AudioAnnotation.objects.filter(audio_file_id=audio_file_id)
    
# Allow user to create , update, view and delete audio annotation by id of the annotation
class AudioAnnotationDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AudioAnnotation.objects.all()
    serializer_class = AudioAnnotationSerializer
    # lookup_field = "id"

    def options(self, request, *args, **kwargs):
        """
        Don't include the view description in OPTIONS responses.
        """
        meta = self.metadata_class()
        data = meta.determine_metadata(request, self)
        data.pop('description')
        return Response(data=data, status=status.HTTP_200_OK)