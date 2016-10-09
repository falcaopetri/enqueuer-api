from rest_framework import permissions


class IsMediaOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view it.
    """


    def has_object_permission(self, request, view, obj):
        # Any permission is only allowed to the media's owner.
        return obj.queue.owner.user == request.user
