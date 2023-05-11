from django.db import models


# Create your models here.

class File(models.Model):
    file = models.TextField()
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class Transcription(models.Model):
    text = models.TextField()
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
