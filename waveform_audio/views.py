import os
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.template import loader
# Create your views here:

def index(request):
    
    return HttpResponse("Hello, world. You're at the waveform index.")


def index_view(request):
    audio_files = ['abc.mp3', 'def.mp3', 'ghi.mp3']
    # get list from Media folder:
    audio_files = os.listdir(settings.MEDIA_ROOT + '\\audio')
    # get only mp3 files or wav files:
    audio_files = [file for file in audio_files if file.endswith('.mp3') or file.endswith('.wav')]
    context = {'audio_files': audio_files}
    # template = loader.get_template('index.html')
    template = 'index.html'
    return render(request, template, context)



def annotate_view(request):
    if request.method == 'POST':
        print(request.POST)
        audio_file = request.POST.get('audio_file')
        print(audio_file)
        # load the audio file:
        context = {'audio_file': audio_file,
                 'audio_file_path': settings.MEDIA_URL + 'audio/' + audio_file
                }
    
        return render(request, 'annotate.html', context)
    else:
       # else return 404 error:
        return HttpResponse("404 error")

    



