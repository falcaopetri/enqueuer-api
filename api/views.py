from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from api.models import User, Queue, Media
from api.serializers import UserSerializer, QueueSerializer, MediaSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'user': reverse('user-list', request=request, format=format),
        'queue': reverse('queue-list', request=request, format=format)
    })


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class QueueViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer


class MediaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
