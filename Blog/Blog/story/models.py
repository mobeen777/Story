from django.db import models
from .validators import validate_file_size


# Create your models here.

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Story(models.Model):
    title = models.CharField(max_length=150)
    details = models.TextField()
    images = models.ManyToManyField("Image", blank=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to=upload_to, validators=[validate_file_size])
