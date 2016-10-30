from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated

from rest_condition import Or, And

from userena.utils import get_user_profile

from friendship.models import Friend

from api.models import UserProfile, Queue, Media
from api.serializers import UserProfileSerializer, QueueSerializer, MediaSerializer
from api.permissions import *
from api.utils import get_users_profiles


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'


class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.none()
    serializer_class = QueueSerializer
    permission_classes = (IsAuthenticated, Or(IsQueueOwner, And(IsFriendsQueue, IsReadOnly)))

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

    def get_object(self):
        obj = get_object_or_404(Queue, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        user = self.request.user
        owner = get_user_profile(user)
        serializer.save(owner=owner)


class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.none()
    serializer_class = MediaSerializer
    permission_classes = (IsAuthenticated, Or(IsMediaOwner, And(IsFriendsMedia, IsPublicMedia, IsReadOnly)))

    def get_queryset(self):
        user = self.request.user
        return Media.objects.filter(queue__owner__user=user)

    def get_object(self):
        obj = get_object_or_404(Media, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_create(self, serializer):
        user = self.request.user
        created_by = get_user_profile(user)
        serializer.save(created_by=created_by)
        

class FriendViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.none()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user = self.request.user
        friends = Friend.objects.friends(user)
        return get_users_profiles(friends)
