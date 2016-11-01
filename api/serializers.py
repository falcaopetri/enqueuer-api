from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from userena.utils import get_user_profile

from friendship.models import Friend

from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from api.models import UserProfile, Queue, Media, MediaService
from api.permissions import IsQueueOwner, IsFriendsQueue
from api.utils import get_users_profiles, are_friends


class FilterRelatedMixin(object):
    """
    Source: https://github.com/tomchristie/django-rest-framework/issues/1985#issuecomment-61871134
    Aim: Allow filtering/permissions on HyperlinkedRelatedField
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field, serializers.RelatedField):
                method_name = 'filter_%s' % name
                try:
                    func = getattr(self, method_name)
                except AttributeError:
                    pass
                else:
                    field.queryset = func(field.queryset)


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


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
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
        model = UserProfile
        fields = ('url', 'username', 'queues')


class MediaSerializer(FilterRelatedMixin, serializers.HyperlinkedModelSerializer):
    queue = serializers.HyperlinkedRelatedField(view_name='queue-detail', queryset=Queue.objects.all())
    media_service = serializers.SlugRelatedField(slug_field='name', queryset=MediaService.objects.all())
    created_by = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True, lookup_field='username')
    tags = TagListSerializerField()

    def filter_queue(self, queryset):
        # TODO this code is equal to UserProfileSerializer.get_queues() -> create a get_user()
        curr_user = None

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            curr_user = request.user
        
        friends = Friend.objects.friends(curr_user)
        # TODO Change privacy check to "is_default_queue" check
        qs = queryset.filter(owner__user__in=friends, privacy=Queue.PRIVATE)
        qs = qs | queryset.filter(owner__user=curr_user)
        return qs

    class Meta:
        model = Media
        fields = ('url', 'created_at', 'created_by', 'queue', 'media_service', 'tags')

    def create(self, validated_data):
        """
            Allows tags saving as suggested on http://stackoverflow.com/a/23056025
        """
        tags = validated_data.pop('tags')
        instance = super().create(validated_data)
        instance.tags.set(*tags)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        """
            Allows tags saving as suggested on http://stackoverflow.com/a/23056025
        """
        tags = validated_data.pop('tags')
        instance.tags.set(*tags)
        instance.save()
        return instance


class MediaServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaService
        fields = ('name')
