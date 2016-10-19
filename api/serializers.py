from django.contrib.auth.models import User as DjangoUser

from rest_framework import serializers

from api.models import User, Queue, Media, MediaService


class QueueListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(privacy=Queue.PUBLIC)
        print(data)
        return super().to_representation(data)


class QueueSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail', lookup_field='username')
    medias = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='media-detail')

    class Meta:
        model = Queue
        #list_serializer_class = QueueListSerializer
        fields = ('url', 'owner', 'name', 'medias', 'privacy')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail', lookup_field='username')
    username = serializers.ReadOnlyField(source='user.username')
    # queues = QueueSerializer(read_only=True, many=True)

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
