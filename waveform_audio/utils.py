import librosa
import json
import os
from django.conf import settings
import numpy as np


def compute_waveform(audio_file, target_fps=20):
    y, sample_rate = librosa.load(audio_file)
    # waveform = audio_data.tolist()
    waveform = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    resampled_waveform = librosa.resample(y = waveform,orig_sr= sample_rate, target_sr = target_fps)

    # Convert the waveform to 8-bit representation
    waveform_8bit = (resampled_waveform - resampled_waveform.min()) / (resampled_waveform.max() - resampled_waveform.min())
    waveform_8bit = (waveform_8bit * 255).astype(np.uint8)
    # waveform_8bit.tolist()
    return waveform_8bit

def save_file_npy(waveform, npy_file):
    np.save(npy_file, waveform)

def convert_np_to_json(np_array):
    waveform = np_array.tolist()
    # convert to dict with json.dump on array?
    waveform = {"waveform": waveform}
    # convert to json:
    waveform = json.dumps(waveform)
    return waveform

def get_waveform_data(audio_file):
    # check if npy file exists:
    folder = settings.MEDIA_ROOT + '/npy/'
    file = audio_file.split('.')[0] + '.npy'
    npy_file = folder + file
    if not os.path.exists(npy_file):
        # if npy file does not exist, create one:
        waveform = compute_waveform(settings.MEDIA_ROOT + '\\audio\\' + audio_file)
        save_file_npy(waveform, npy_file)
    else:
        with open(folder + file, 'rb') as f:
            print("loading the waveform from npy file")
            waveform = np.load(f)
    waveform = convert_np_to_json(waveform)
    # assert isinstance(waveform, str)
    return waveform