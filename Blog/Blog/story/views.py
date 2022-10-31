from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *


# Create your views here.

class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StoryImageSerializer

    def list(self, request, *args, **kwargs):
        queryset = Story.objects.all()
        serializer = StoryImageSerializer(queryset, many=True, context={'request': request})
        return Response({"News": serializer.data}, status=200)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, context={'request': request})
        return Response({"News": serializer.data}, status=200)

    def create(self, request, *args, **kwargs):
        serializer = StoryImageSerializer(data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer_ = serializer.save()

        for image in request.FILES.getlist("images"):
            img = ImageSerializer(data={"image": image})
            if img.is_valid():
                img = img.save()
                serializer_.story.add(img)
        serializer_.save()

        return Response({"News": serializer.data}, status=201)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({"News": serializer.data}, status=200)
