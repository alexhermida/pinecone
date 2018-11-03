from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from rest_framework import serializers

from core import models, services


class ChoiceSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()


# Serializers define the API representation.
class UserProfileSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'fullname')
        read_only_fields = ('id', 'username', 'fullname')

    def get_fullname(self, instance):
        return f'{instance.first_name} {instance.last_name}'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class EventSerializer(serializers.HyperlinkedModelSerializer):
    link = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    start = serializers.DateTimeField(required=False)
    google_calendar_published = serializers.BooleanField(required=False)

    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail'
    )

    class Meta:
        model = models.Event
        fields = ('id', 'url', 'title', 'description', 'group', 'link',
                  'location', 'start', 'duration', 'status', 'user', 'created',
                  'modified', 'google_calendar_published', 'google_event_id',
                  'google_event_htmllink')
        read_only_fields = ('google_event_htmllink',)


class EventCreateSerializer(serializers.ModelSerializer):
    link = serializers.CharField(required=False, allow_blank=True)
    location = serializers.CharField(required=False, allow_blank=True)
    start = serializers.DateTimeField(required=False)
    google_calendar_published = serializers.BooleanField(required=False)

    user = serializers.HyperlinkedRelatedField(
        read_only=True,
        view_name='user-detail'
    )

    class Meta:
        model = models.Event
        fields = ('id', 'url', 'title', 'description', 'group', 'link',
                  'location', 'start', 'duration', 'status', 'user', 'created',
                  'modified', 'google_calendar_published', 'google_event_id')

        read_only_fields = 'created', 'modified', 'google_event_id'

    def save(self):
        user = self.context.get("request").user \
            if 'request' in self.context else None
        self.validated_data['user'] = user

        if self.validated_data.get('google_calendar_published'):
            event_id, html_link = self.create_google_calendar_event()
            if event_id:
                self.validated_data['google_event_id'] = event_id
                self.validated_data['google_event_htmllink'] = html_link
                self.validated_data['status'] = 'published'

        return super().save()

    def create_google_calendar_event(self):
        """
        Create event in Google Calendar
        """
        # TODO Refactor to celery
        gcalendar = services.GoogleCalendarService()
        gcalendar.initialize()

        group = self.validated_data.get('group')
        title = self.validated_data.get('title')
        summary = f'{group} - {title}'
        description = self.validated_data.get('description')
        location = self.validated_data.get('location')
        startime = self.validated_data.get('start').isoformat()
        endtime = self.validated_data.get('end').isoformat()

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

        created_event = gcalendar.create_event(event)
        event_id = created_event.get('id')
        event_htmllink = created_event.get('htmlLink')

        return event_id, event_htmllink

    def validate(self, data):
        """
        Check if there are start&end datetimes to publish in Google Calendar.
        """
        start = data.get('start')
        duration = data.get('duration')

        if start and not duration:
            raise serializers.ValidationError(
                _('If you enter start date you must enter the duration'))

        if not data.get('google_calendar_published'):
            return data

        if not start or not duration:
            raise serializers.ValidationError(
                _('To publish in Google Calendar you must enter start '
                  'time and duration'))

        return data
