from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import json
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from .dao import sync_audio_files, get_audio_files_queryset, get_audio_file_obj_by_name
from .dao import create_audio_annotation, get_audio_annotations_queryset
from .models import AudioFile


def update_database_view(request):
    if request.method == "POST":
        sync_audio_files()
        # after doing this redirect to index page that will pull data from database:
        return redirect("index")
    else:
        return HttpResponse("404 error")


def index_view(request):
    audio_files = list(get_audio_files_queryset().values_list('file', flat=True))
    if not audio_files:
        sync_audio_files()
        audio_files = list(get_audio_files_queryset().values_list('file', flat=True))
    context = {"audio_files": audio_files}
    template = "index.html"
    return render(request, template, context)


def annotate_view(request):
    if request.method == "POST":
        audio_file = request.POST.get("audio_file")
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

        table = pd.DataFrame(annotation_table)
        # get delta time:
        table["start_time"] = pd.to_datetime(table["start_time"], unit="s").dt.time
        table["end_time"] = pd.to_datetime(table["end_time"], unit="s").dt.time
        # save annotations to database:
        audio_file_obj = get_audio_file_obj_by_name(audio_file)
        for index, row in table.iterrows():
            create_audio_annotation(
                audio_file_obj,
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
        # get annotations from database:
        annotations = get_audio_annotations_queryset(audio_file__file=audio_file)
        # convert annotations to pandas dataframe:
        annotations = pd.DataFrame(
            list(
                annotations.values(
                    "audio_file__file", "start_time", "end_time", "annotation", "timestamp", "id"
                )
            )
        )
        if annotations.empty:
            return JsonResponse({"message": "No annotations found"})
        template = "annotations_dashboard.html"
        annotations['start_time'] = annotations['start_time'].apply(lambda x: x.strftime('%H:%M:%S'))
        annotations['end_time'] = annotations['end_time'].apply(lambda x: x.strftime('%H:%M:%S'))
        context = {"annotations": annotations.to_dict(orient='records')}
        return render(request, template, context)
        # return JsonResponse({"message": "Annotations have been saved", "annotations": annotations.to_json()})
    else:
        return HttpResponse("404 error")
