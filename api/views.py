from rest_framework import generics

from api.models import User, Queue
from api.serializers import UserSerializer, QueueSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class QueueList(generics.ListCreateAPIView):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
