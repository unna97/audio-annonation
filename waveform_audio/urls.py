"""waveform_audio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "waveform_audio"

urlpatterns = [
    path("admin/", admin.site.urls),
    
    
    path("", views.AudioFileAvailableView.as_view(), name="index"),

    path("annotate/", views.annotate_view, name="annotate"),
    path("save_annotations/", views.save_annotations, name="save_annotations"),
    path("update_database/", views.update_database, name="update_database"),
    path("clean_database/", views.clean_database, name="clean_database"),
    # example url:
    # API urls:
    path("api/", include("api.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
