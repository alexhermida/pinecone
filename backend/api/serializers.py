from django.contrib.auth.models import User

from rest_framework import serializers

from core import models, services


class ChoiceSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    link = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    google_calendar_published = serializers.BooleanField(required=False)

    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail'
    )

    class Meta:
        model = models.Event
        fields = ('id', 'url', 'description', 'group', 'link', 'location',
                  'start', 'end', 'status', 'user', 'created', 'modified',
                  'google_calendar_published')


class EventCreateSerializer(serializers.ModelSerializer):
    link = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    google_calendar_published = serializers.BooleanField(required=False)

    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail'
    )

    class Meta:
        model = models.Event
        fields = ('id', 'url', 'description', 'group', 'link', 'location',
                  'start', 'end', 'status', 'user', 'created', 'modified',
                  'google_calendar_published')

        read_only_fields = 'created', 'modified'

    def save(self):
        if self.validated_data.get('google_calendar_published'):
            self.create_google_calendar_event(self.validated_data)
        user = self.context.get("request").user

        return super().save(user=user)

    def create_google_calendar_event(self, data):
        gCalendar = services.GoogleCalendarService()
        gCalendar.initialize()

        group = data['group']
        title = data['title']
        summary = f'{group} - {title}'
        description = data['description']
        location = data['location']
        startime = data['start'].isoformat()
        endtime = data['end'].isoformat()

        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': startime,
            },
            'end': {
                'dateTime': endtime,
            },
        }

        gCalendar.create_event(event)
