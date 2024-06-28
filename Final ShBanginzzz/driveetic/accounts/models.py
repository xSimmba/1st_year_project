
from django.db import models
from updownfunks.models import File

class StaffMember(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    file = models.ForeignKey(File, on_delete=models.CASCADE)  # Use the imported File model

    def __str__(self):
        return self.name
