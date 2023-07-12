from waveform_audio.models import AudioFile, AudioAnnotation
from waveform_audio.utils import get_stored_audio_files


def get_audio_files_queryset(limit: int = None, offset: int = None, **filters):
    queryset = AudioFile.objects.filter(**filters).all()
    if offset is not None:
        queryset = queryset[offset:]
    if limit is not None:
        queryset = queryset[:limit + (offset or 0)]
    return queryset


def get_audio_file_obj_by_name(file_name):
    return AudioFile.objects.get(file=file_name)


def remove_audio_files_entries(audio_files):
    for file in audio_files:
        AudioFile.objects.filter(file=file).delete()


def add_audio_files_entries(audio_files):
    for file in audio_files:
        AudioFile.objects.create(file=file)


def sync_audio_files():
    audio_files = set(get_stored_audio_files())
    audio_files_qs = get_audio_files_queryset()
    db_audio_files = set(audio_files_qs.values_list('file', flat=True))

    to_remove = db_audio_files - db_audio_files.intersection(audio_files)
    remove_audio_files_entries(to_remove)

    to_add = audio_files - db_audio_files.intersection(audio_files)
    add_audio_files_entries(to_add)


def create_audio_annotation(audio_file_obj, start_time, end_time, annotation):
    return AudioAnnotation.objects.create(
        audio_file=audio_file_obj,
        start_time=start_time,
        end_time=end_time,
        annotation=annotation,
    )


def get_audio_annotations_queryset(limit: int = None, offset: int = None, **filters):
    queryset = AudioAnnotation.objects.filter(**filters).all()
    if offset is not None:
        queryset = queryset[offset:]
    if limit is not None:
        queryset = queryset[:limit + (offset or 0)]
    return queryset

