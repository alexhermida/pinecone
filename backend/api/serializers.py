from django.contrib.auth.models import User

from rest_framework import serializers

from core import models


class ChoiceSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Event
        fields = ('id', 'url', 'description', 'group', 'link', 'location', 'status',
                  'created', 'modified')
