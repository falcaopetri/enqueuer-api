from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated

from userena.utils import get_user_profile

from friendship.models import Friend

from api.models import User, Queue, Media
from api.serializers import UserSerializer, QueueSerializer, MediaSerializer
from api.permissions import IsMediaOwner
from api.utils import get_users_profiles

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'


class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.none()
    serializer_class = QueueSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        """
            self.request.user contains a django-userena's user, provided by
            AUTHENTICATION_BACKENDS variable on enqueuer's settings.py
            (reference: http://www.django-rest-framework.org/api-guide/authentication/)

            In order to get this django-userena's user, I'm using get_user_profile(User),
            declared on django-userena's utils.py
            (https://github.com/bread-and-pepper/django-userena/blob/master/userena/utils.py)
        """
        # TODO: that's not the actual expected behavior
        # We should be able to see PUBLIC queues of FRIENDS of mine
        user = self.request.user
        owner = get_user_profile(user)
        return owner.queues.all()

    def perform_create(self, serializer):
        user = self.request.user
        owner = get_user_profile(user)
        serializer.save(owner=owner)


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.none()
    serializer_class = MediaSerializer
    permission_classes = (IsAuthenticated, IsMediaOwner)

    def get_queryset(self):
        user = self.request.user
        return Media.objects.filter(queue__owner__user=user)


class FriendViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        friends = Friend.objects.friends(user)
        return get_users_profiles(friends)
