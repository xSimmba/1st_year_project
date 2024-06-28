from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_orphan = models.BooleanField()
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE, null=True, blank=True, related_name='files')
    
    def __str__(self):
        return self.name


class Folder(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return self.name

    @property
    def folder_path(self):
        if self.parent_folder:
            return f"{self.parent_folder.folder_path}/{self.name}"
        else:
            return self.name