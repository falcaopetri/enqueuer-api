from django.contrib.auth.models import User as DjangoUser

from rest_framework import serializers

from api.models import User, Queue, Media, MediaService


class QueueSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail', lookup_field='username')
    medias = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='media-detail')

    class Meta:
        model = Queue
        fields = ('url', 'owner', 'medias', )

class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = User
        fields = ('username', 'queues')

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('url', 'created', 'queue', 'media_service')

class MediaServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaService
        fields = ('name')
