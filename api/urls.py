from django.urls import path, include

from . import views

urlpatterns = [
    path('audio_annotations/', views.AudioAnnotationViewSet.as_view()),
    #allow for audio_file to be passed as a query parameter:
    path('audio_annotations/<int:audio_file>/', views.AudioAnnotationViewSet.as_view()),
]