from django.contrib.auth.models import User as DjangoUser

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from userena.utils import get_user_profile

from api.models import User, Queue, Media, MediaService
from api.permissions import IsQueueOwner, IsFriendsQueue
from api.utils import are_friends



class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    Source: http://www.django-rest-framework.org/api-guide/serializers/#dynamically-modifying-fields
    """

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class QueueSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail', lookup_field='username')
    medias = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='media-detail')

    class Meta:
        model = Queue
        fields = ('url', 'owner', 'name', 'medias', 'privacy')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='username')
    username = serializers.ReadOnlyField(source='user.username')
    queues = serializers.SerializerMethodField()

    def get_queues(self, user):
        curr_user = None

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            curr_user = request.user

        qs = Queue.objects.none()
        if user.user == curr_user:
            # Is the owner
            qs = user.queues.all()
        elif are_friends(user.user, curr_user):
            # Are friends, only show Public Queues
            qs = user.queues.filter(privacy=Queue.PUBLIC)
        
        serializer = QueueSerializer(instance=qs, read_only=True, many=True, context=self.context, fields=['url', 'name'])
        return serializer.data

    class Meta:
        model = User
        fields = ('url', 'username', 'queues')

class MediaSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: filter user's queues
    queue = serializers.HyperlinkedRelatedField(view_name='queue-detail', queryset=Queue.objects.all())
    media_service = serializers.SlugRelatedField(slug_field='name', queryset=MediaService.objects.all())

    class Meta:
        model = Media
        fields = ('url', 'created', 'queue', 'media_service')

class MediaServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaService
        fields = ('name')
