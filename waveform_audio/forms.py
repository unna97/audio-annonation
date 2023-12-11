# import crispy_forms.helper as crispy_helper
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


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
