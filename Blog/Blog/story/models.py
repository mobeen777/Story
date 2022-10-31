from django.db import models
from rest_framework.reverse import reverse
from .validators import validate_file_size


# Create your models here.

def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Story(models.Model):
    title = models.CharField(max_length=150)
    details = models.TextField()

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to=upload_to, validators=[validate_file_size])
    story = models.ForeignKey("Story", blank=True, on_delete=models.CASCADE, related_name='story', null=True)

    # def get_absolute_url(self):
    #     return reverse('image', kwargs={'id': self.id})
