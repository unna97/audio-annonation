from django.core.files.storage import FileSystemStorage

ACCEPTED_FORMATS = {"mp3", "wav", "mp4"}


def get_stored_audio_files():
    files = set(FileSystemStorage().listdir("audio")[1])
    # get only mp3 files or wav files:
    audio_files = []
    for file in files:
        file_name_suffix = file.split('.')[-1]
        if file_name_suffix in ACCEPTED_FORMATS:
            audio_files.append(file)
    return audio_files
