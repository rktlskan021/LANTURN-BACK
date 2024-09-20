from .models import Link
from .serializers import LinkSerializer
from rest_framework import viewsets


# Create your views here.
class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer