import os
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.template import loader
import json
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .models import AudioFile, AudioAnnotation


def update_database(request):
    if request.method == "POST":
        audio_files = FileSystemStorage().listdir("audio")[1]
        accepted_format = ["mp3", "wav", "mp4"]
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
    try:
        audio_files = AudioFile.objects.all()
    except AudioFile.DoesNotExist:
        # call update_database function:
        update_database(request)
        audio_files = AudioFile.objects.all()

    audio_files = [file.file.name for file in audio_files]
    context = {"audio_files": audio_files}
    template = "index.html"
    return render(request, template, context)


def annotate_view(request):
    if request.method == "POST":
        print(request.POST)
        audio_file = request.POST.get("audio_file")
        print(audio_file)
        # get waveform data:
        labels = ["laugh", "crowd", "other"]
        # load the audio file:
        context = {
            "audio_file": audio_file,
            "audio_file_path": settings.MEDIA_URL + "audio/" + audio_file,
            "labels": labels,
        }

        return render(request, "annotate.html", context)
    else:
        # else return 404 error:
        return HttpResponse("404 error")


@csrf_exempt
def save_annotations(request):
    if request.method == "POST":
        data = json.loads(request.body)
        annotation_table = json.loads(data.get("annotation_table"))
        audio_file = data.get("audio_file_path").split("/")[-1]

        print(annotation_table)
        table = pd.DataFrame(annotation_table)
        print(table)
        print(audio_file)
        # get delta time:
        table["start_time"] = pd.to_datetime(table["start_time"], unit="s").dt.time
        table["end_time"] = pd.to_datetime(table["end_time"], unit="s").dt.time
        # save annotations to database:
        for index, row in table.iterrows():
            AudioAnnotation.objects.create(
                audio_file=AudioFile.objects.get(file=audio_file),
                start_time=row["start_time"],
                end_time=row["end_time"],
                annotation=row["label"],
            )
        # provide a popup message that annotations have been saved:
        return JsonResponse({"message": "Annotations have been saved"})
    return JsonResponse({"message": "404 error"})

def clean_database(request):
    if request.method == "POST":
        # get annotations from database for the current audio file:
        audio_file = request.POST.get("audio_file")
        print(audio_file)
        # get annotations from database:
        annotations = AudioAnnotation.objects.filter(audio_file__file=audio_file)
        # convert annotations to pandas dataframe:
        annotations = pd.DataFrame(
            list(
                annotations.values(
                    "audio_file__file", "start_time", "end_time", "annotation", "timestamp", "id"
                )
            )
        )
        print(annotations)
        if annotations.empty:
            return JsonResponse({"message": "No annotations found"})
        template = "annotations_dashboard.html"
        annotations['start_time'] = annotations['start_time'].apply(lambda x: x.strftime('%H:%M:%S'))
        annotations['end_time'] = annotations['end_time'].apply(lambda x: x.strftime('%H:%M:%S'))
        context = {"annotations": annotations.to_dict(orient='records')}
        return render(request, template, context)
        #return JsonResponse({"message": "Annotations have been saved", "annotations": annotations.to_json()})
    else:
        return HttpResponse("404 error")
