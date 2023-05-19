import librosa
import json
import os
from django.conf import settings
import numpy as np


def compute_waveform(audio_file):
    audio_data, sample_rate = librosa.load(audio_file, sr=None)
    waveform = audio_data.tolist()
    return waveform

def save_file_json(waveform, audio_file):
    json_data = {"waveform": waveform}
    json_file = audio_file.split('.')[0] + '.json'
    with open(settings.MEDIA_ROOT + '\\json\\' + json_file, 'w') as f:
        json.dump(json_data, f)

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
    # check if json file exists:
    folder = settings.MEDIA_ROOT + '/npy/'
    file = audio_file.split('.')[0] + '.npy'
    npy_file = folder + file
    if not os.path.exists(npy_file):
        # if json file does not exist, create one:
        waveform = compute_waveform(settings.MEDIA_ROOT + '\\audio\\' + audio_file)
        save_file_npy(waveform, npy_file)
    else:
        with open(folder + file, 'rb') as f:
            print("loading the waveform from npy file")
            waveform = np.load(f)
    waveform = convert_np_to_json(waveform)
    # assert isinstance(waveform, str)
    return waveform