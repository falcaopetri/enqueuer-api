from rest_framework import permissions

from api.models import Queue
from api.utils import are_friends


class IsMediaOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view it.
    """


    def has_object_permission(self, request, view, obj):
        # Any permission is only allowed to the media's owner.
        return obj.queue.owner.user == request.user


class IsQueueOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an queue to view it.
    """

    def has_object_permission(self, request, view, obj):
        # Any permission is only allowed to the queues's owner.
        return obj.owner.user == request.user


class IsFriendsQueue(permissions.BasePermission):
    """
    Object-level permission to allow a user to see a friend's public queue.
    """

    def has_object_permission(self, request, view, obj):
        friends = are_friends(request.user, obj.owner.user)
        return friends and obj.privacy == Queue.PUBLIC


class IsPublicMedia(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Any permission is only allowed to the queues's owner.
        return obj.queue.privacy == Queue.PUBLIC


class IsFriendsMedia(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        friends = are_friends(request.user, obj.queue.owner.user)
        return friends


class IsFriendsQueue(permissions.BasePermission):
    """
    Object-level permission to allow a user to see a friend's public queue.
    """

    def has_object_permission(self, request, view, obj):
        # Any permission is only allowed to the queues's owner.
        friends = are_friends(request.user, obj.owner.user)
        return friends and obj.privacy == Queue.PUBLIC


class IsReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow SAFE methods.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return request.method in permissions.SAFE_METHODS
