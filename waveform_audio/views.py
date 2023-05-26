import os
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.template import loader
from .utils import get_waveform_data
import json
from django.views.decorators.csrf import csrf_exempt
import pandas as pd

# Create your views here:

def index(request):
    
    return HttpResponse("Hello, world. You're at the waveform index.")


def index_view(request):
    # get list from Media folder:
    audio_files = FileSystemStorage().listdir('audio')[1]
    # get only mp3 files or wav files:
    audio_files = [file for file in audio_files if file.endswith('.mp3') or file.endswith('.wav')]
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
        table = pd.DataFrame(annotation_table)
        # Process the annotation_table data as needed
        print(annotation_table)
        print(table)
        # Save the annotation_table data to a file:
        table.to_csv(settings.MEDIA_ROOT + '/annotations.csv', index=False)
      
        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error"})



