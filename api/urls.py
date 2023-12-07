from django.urls import path
from . import views

urlpatterns = [
    path('audio-files/', views.AudioFileListAPIView.as_view(), name='audio-file-list'),
    path('audio-files/<int:pk>/', views.AudioFileDetailAPIView.as_view(), name='audio-file-detail'),
    path('audio-files/upload/', views.AudioFileUploadAPIView.as_view(), name='audio-file-upload'),
    path('audio-files/<int:audio_file_id>/annotations/', views.AudioAnnotationListAPIView.as_view(), name='audio-annotation-list'),
    path('audio-files/<int:audio_file_id>/annotations/<int:pk>/', views.AudioAnnotationDetailAPIView.as_view(), name='audio-annotation-detail'),

]