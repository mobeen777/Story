from rest_framework import serializers
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class StoryImageSerializer(serializers.ModelSerializer):
    story = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'title', 'details', 'story']