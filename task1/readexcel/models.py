from django.db import models

import uuid

# Create your models here.
def user_directory_path(instance, filename):
    a = str(uuid.uuid1())
    return 'files/{a}_{filename}'

class ExcelFile(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    