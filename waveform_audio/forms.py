# import crispy_forms.helper as crispy_helper
from django import forms
from django.utils.translation import gettext_lazy as _

from waveform_audio.models import AudioFile, Subtitle
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from waveform_audio import utils
import mimetypes


# url: https://stackoverflow.com/questions/24783275/django-form-with-choices-but-also-with-freetext-option?noredirect=1&lq=1
class AudioFileForm(forms.Form):
    audio_file = forms.FileField(
        label="Select a file",
        help_text="insert an audio file",
        widget=forms.FileInput(attrs={"accept": "audio/*"}),
    )
    artist_names = forms.CharField(
        label="Artist name(s)",
        help_text="insert artist name(s)",
        widget=forms.TextInput(attrs={"placeholder": "artist name(s)"}),
    )

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = "POST"
        helper.inputs.append(Submit("submit", "Submit"))
        return helper


class AudioModelFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ["file"]
        labels = {
            "file": "Select a file",
        }
        help_texts = {
            "file": "insert an audio file",
        }
        widgets = {
            "file": forms.FileInput(attrs={"accept": "audio/wav,audio/mp3,audio/mp4"}),
        }

    def clean_file(self):
        audio_file = self.cleaned_data.get("file")
        print("clean_file is called")
        if audio_file:
            valid_mime_types = ["audio/mpeg", "audio/wav", "audio/mp3"]
            mime_type, _ = mimetypes.guess_type(audio_file.name)
            if mime_type is None or mime_type not in valid_mime_types:
                raise forms.ValidationError(
                    _("Invalid audio file type"), code="invalid_file_type"
                )
        return audio_file


class SubtitleFileForm(forms.Form):
    subtitle_file = forms.FileField(
        label="Select a subtitle file",
        help_text="insert a subtitle file",
        widget=forms.FileInput(attrs={"accept": ".srt"}),
    )

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_method = "POST"
        helper.inputs.append(Submit("submit", "Submit"))
        return helper

    def clean_subtitle_file(self):
        subtitle_file = self.cleaned_data.get("subtitle_file")
        if subtitle_file:
            try:
                self.subtitle_texts = utils.process_subtitle_file(subtitle_file)
            except Exception as e:
                raise forms.ValidationError(f"Error processing subtitle file: {str(e)}")
        return subtitle_file

    def save(self, audio_file_instance):
        if hasattr(self, "subtitle_texts"):
            subtitles = [
                Subtitle.objects.create(
                    audio_file=audio_file_instance,
                    start_time=subtitle["start_time"],
                    end_time=subtitle["end_time"],
                    content=subtitle["content"],
                )
                for subtitle in self.subtitle_texts
            ]
            return subtitles
        return []
