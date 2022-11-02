from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from .models import *
from .utils import save_paper


# Create your views here.

class PaperViewset(viewsets.ModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer

    def create(self, request, *args, **kwargs):
        save_paper(request.FILES['paper'])

        return Response(status=200)
