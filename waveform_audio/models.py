from django.db import models

class AudioFile(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to='audio/')
    timestamp = models.DateTimeField(auto_now_add=True)
