from ast import Sub
from email import errors
from math import e
from os import error
from re import template
from typing import Any
import requests
import json

import pandas as pd

# from django.shortcuts import render
from django.http import HttpResponse, JsonResponse  # HttpResponse,
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.shortcuts import redirect, render


from waveform_audio.models import AudioFile, AudioAnnotation, Subtitle
from waveform_audio.forms import AudioFileForm, AudioModelFileForm, SubtitleFileForm
from waveform_audio import utils


@csrf_exempt
def save_annotations(request):
    if request.method == "POST":
        data = json.loads(request.body)
        annotation_table = json.loads(data.get("annotation_table"))
        # audio_file = data.get("audio_file_path").split("/")[-1]
        audio_id = data.get("audio_id")
        print(annotation_table)
        table = pd.DataFrame(annotation_table)
        print(table)
        # get delta time:
        table["start_time"] = pd.to_datetime(table["start_time"], unit="s").dt.time
        table["end_time"] = pd.to_datetime(table["end_time"], unit="s").dt.time
        # save annotations to database:
        for index, row in table.iterrows():
            AudioAnnotation.objects.create(
                audio_file=AudioFile.objects.get(id=audio_id),
                start_time=row["start_time"],
                end_time=row["end_time"],
                annotation=row["label"],
            )
        # provide a popup message that annotations have been saved:
        return JsonResponse({"message": "Annotations have been saved"})
    return JsonResponse({"message": "404 error"})


# use template view to render the annotations dashboard:
class AudioFileAvailableView(TemplateView):
    template_name = "index.html"

    # time the function:
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        audio_files = AudioFile.objects.all()
        context["audio_files"] = audio_files

        return context
    

class UploadAudioAndSubtitleView(FormView):
    template_name = 'upload_audio_subtitle.html'
    audio_form_class = AudioModelFileForm
    subtitle_form_class = SubtitleFileForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        audio_form = self.audio_form_class()
        subtitle_form = self.subtitle_form_class()
        return render(request, self.template_name, {'audio_form': audio_form, 'subtitle_form': subtitle_form})

    def post(self, request, *args, **kwargs):
        audio_form = self.audio_form_class(request.POST, request.FILES)
        subtitle_form = self.subtitle_form_class(request.POST, request.FILES)
        
        if audio_form.is_valid():
            audio_file_instance = audio_form.save()
            # if the file is already in the database:
            if AudioFile.objects.filter(file=audio_file_instance.file).exists():
                audio_file_instance = AudioFile.objects.get(file=audio_file_instance.file)
            
            if subtitle_form.is_valid():
                subtitle_file = request.FILES['subtitle_file']
                subtitle_texts = utils.process_subtitle_file(subtitle_file)
                subtitle_data = self.save_subtitle_data(audio_file_instance, subtitle_texts)
        else:
            # show the errors in the form:
            print(audio_form.errors)
            print(subtitle_form.errors)
            errors = audio_form.errors | subtitle_form.errors
            return JsonResponse({"message": "","errors":errors})
        
        return redirect(self.success_url)

    def save_subtitle_data(self, audio_file_instance, subtitle_texts):
       # save the subtitle data to the database:
        subtitle_data = [ {**s, "audio_file": audio_file_instance} for s in subtitle_texts ]
        #TODO: Figure out how to do bulk create
        subtitle_data_obj = [ Subtitle.objects.create(**s) for s in subtitle_data ]

        return subtitle_data_obj
    



class UploadAudioFileView(FormView):
    template_name = "upload.html"
    form_class = AudioFileForm
    # Success calls the api view of the AudioFileListAPIView
    success_url = "/api/audio-files/"
    # success_url = reverse('api:audio-file-upload')

    def form_valid(self, form):
        # save the file to the database:
        audio_file = form.cleaned_data["audio_file"]
        audio_file_name = audio_file.name

        # Prepare the API endpoint URL
        if form.is_valid():
            api_url = reverse("api:audio-file-upload")
            api_url_with_scheme = self.request.build_absolute_uri(api_url)

            file = {"file": (audio_file_name, audio_file)}
            response = requests.post(api_url_with_scheme, files=file)
            if response.status_code == 201:
                return super().form_valid(form)
            return self.form_invalid(form, api_response=response.json())

        return super().form_invalid(form)

    def form_invalid(self, form, api_response=None):
        # get a popup message on the html page that the file is not valid:
        if api_response not in (None, {}):
            form.add_error(None, api_response)

        return super().form_invalid(form)


# show save annotations for the selected audio file:
@method_decorator(require_http_methods(["POST"]), name="dispatch")
class AudioAnnotationsTableView(TemplateView):
    template_name = "annotations_dashboard.html"
    # this will be called by a POST request i.e when the user clicks on the button:

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # get the audio file id:
        audio_file_id = self.request.POST.get("audio_id")
        print(audio_file_id)

        # TODO: Use API to get the annotations
        # get annotations from database by id:
        annotations = AudioAnnotation.objects.filter(audio_file__id=audio_file_id)

        annotations = pd.DataFrame(
            list(
                annotations.values(
                    "audio_file__file",
                    "start_time",
                    "end_time",
                    "annotation",
                    "timestamp",
                    "id",
                )
            )
        )
        print(annotations)
        if annotations.empty:
            message = "No annotations found"
            context["message"] = message
            return context

        annotations["start_time"] = annotations["start_time"].apply(
            lambda x: x.strftime("%H:%M:%S")
        )
        annotations["end_time"] = annotations["end_time"].apply(
            lambda x: x.strftime("%H:%M:%S")
        )
        context = {"annotations": annotations.to_dict(orient="records")}

        return context

    # this a post only view:
    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))


class AnnotateAudioFileView(TemplateView):
    template_name = "annotate.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        # get the audio file id:
        audio_file_id = self.request.POST.get("audio_file")
        print(audio_file_id)
        audio_file = AudioFile.objects.get(id=audio_file_id)
        context["audio_file"] = audio_file
        context["audio_file_path"] = audio_file.file.url
        labels = ["laugh", "crowd", "other"]
        context["labels"] = labels
        return context

    def post(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))
