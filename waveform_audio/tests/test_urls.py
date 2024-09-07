import pytest
from django.urls import reverse, resolve
from django.conf import settings

@pytest.mark.django_db
class TestURLs:
    def test_admin_url(self):
        url = reverse('admin:index')
        assert resolve(url).view_name == 'admin:index'

    def test_index_url(self):
        url = reverse('index')
        assert resolve(url).view_name == 'index'
        assert resolve(url).func.view_class.__name__ == 'AudioFileAvailableView'

    def test_annotate_url(self):
        url = reverse('annotate')
        assert resolve(url).view_name == 'annotate'
        assert resolve(url).func.view_class.__name__ == 'AnnotateAudioFileView'

    def test_save_annotations_url(self):
        #TODO: Add class based + form based view for this URL
        url = reverse('save_annotations')
        assert resolve(url).view_name == 'save_annotations'
        assert resolve(url).func.__name__ == 'save_annotations'

    def test_upload_url(self):
        url = reverse('upload')
        assert resolve(url).view_name == 'upload'
        assert resolve(url).func.view_class.__name__ == 'UploadAudioAndSubtitleView'

    def test_clean_database_url(self):
        url = reverse('clean_database')
        assert resolve(url).view_name == 'clean_database'
        assert resolve(url).func.view_class.__name__ == 'AudioAnnotationsTableView'
 
    def test_api_url(self):
        url = reverse('api:api-root')
        assert resolve(url).namespace == 'api'

    def test_media_url(self):
        url = f"{settings.MEDIA_URL}test.txt"
        assert resolve(url).func.__name__ == 'serve'
        assert resolve(url).kwargs['document_root'] == settings.MEDIA_ROOT