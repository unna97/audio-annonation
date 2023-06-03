import os
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.template import loader
from .utils import get_waveform_data
import json
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .models import AudioFile

# Create your views here:

def update_database(request):
    if request.method == 'POST':
        audio_files = FileSystemStorage().listdir('audio')[1]
        accepted_format = ['mp3', 'wav', 'mp4']
        # get only mp3 files or wav files:
        for file in audio_files:
            for format in accepted_format:
                if file.endswith(format):
                    # check if file is in database:
                    print("checking if file is in database")
                    if not AudioFile.objects.filter(file=file).exists():
                        # add file to database:
                        print("adding file to database")
                        AudioFile.objects.create(file=file)
        # after doing this redirect to index page that will pull data from database:
        return redirect("index")
    else:
        return HttpResponse("404 error")
              



def index_view(request):
    audio_files = AudioFile.objects.all()
    audio_files = [file.file.name for file in audio_files]
    context = {'audio_files': audio_files}
    template = 'index.html'
    return render(request, template, context)



def annotate_view(request):
    if request.method == 'POST':
        print(request.POST)
        audio_file = request.POST.get('audio_file')
        print(audio_file)
        # get waveform data:
        waveform = get_waveform_data(audio_file)
            
        # load the audio file:
        context = {'audio_file': audio_file,
                   'audio_file_path': settings.MEDIA_URL + 'audio/' + audio_file,
                   'waveform': waveform
                }
    
        return render(request, 'annotate.html', context)
    else:
       # else return 404 error:
        return HttpResponse("404 error")

@csrf_exempt
def save_annotations(request):
    
    if request.method == "POST":
        # annotation_table = request.POST.get("annotation_table")
        data = json.loads(request.body)
        annotation_table = json.loads(data.get("annotation_table"))
        # table = pd.DataFrame(annotation_table)
        # dont read teh time stamp column as a date time:
        # Process the annotation_table data as needed
        print(annotation_table)
        table = pd.DataFrame(annotation_table)
        print(table)
        # Save the annotation_table data to a sql database:
        # table.to_sql('annotation_table', con=settings.DATABASES['default'], if_exists='append', index=False)
      
        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"})



