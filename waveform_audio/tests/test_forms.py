import pytest
from waveform_audio.forms import SubtitleFileForm, AudioModelFileForm


@pytest.mark.django_db
class TestSubtitleFileForm:
    def test_subtitle_file_form_valid(self, subtitles_file_1):
        form_data = {"subtitle_file": subtitles_file_1}
        form = SubtitleFileForm(data={}, files=form_data)
        assert form.is_valid()

    def test_subtitle_file_form_invalid(self, audio_file_1):
        form_data = {"subtitle_file": audio_file_1}
        form = SubtitleFileForm(data={}, files=form_data)
        assert not form.is_valid()

    def test_subtitle_file_form_invalid_empty(self):
        form_data = {}
        form = SubtitleFileForm(data={}, files=form_data)
        assert not form.is_valid()


@pytest.mark.django_db
class TestAudioModelFileForm:
    def test_audio_model_file_form_valid(self, audio_file_1):
        form_data = {"file": audio_file_1}
        form = AudioModelFileForm(data={}, files=form_data)
        assert form.is_valid()

    def test_audio_model_file_form_invalid(self, subtitles_file_1):
        form_data = {"file": subtitles_file_1}
        form = AudioModelFileForm(data={}, files=form_data)
        assert not form.is_valid(), "The form should be invalid"
        # check the exception raised:
        assert form.errors["file"][0] == "Invalid audio file type"
