from django.contrib.auth.models import User as DjangoUser

from rest_framework import serializers

from api.models import User, Queue, Media, MediaService


class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoUser
        fields = ('username')

class QueueSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.user.username')
    #medias = serializers.PrimaryKeyRelatedField(many=True, queryset=Media.objects.all())
 
    class Meta:
        model = Queue
        fields = ('owner', 'medias', )

class UserSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    # TODO add queues field
    # queues = serializers.HyperlinkedRelatedField(queryset=Queue.objects.all(), view_name='queues-detail', many=True)
    # queues = QueueSerializer

    class Meta:
        model = User
        # TODO add queues field
        fields = ('id', 'user')

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('url', 'created', 'queue', 'media_service')

class MediaServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaService
        fields = ('name')
