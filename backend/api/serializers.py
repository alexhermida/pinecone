from datetime import timedelta

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
                  'location', 'start', 'end', 'duration', 'status', 'user',
                  'created', 'modified', 'google_calendar_published',
                  'google_event_id', 'google_event_htmllink')
        read_only_fields = ('google_event_id', 'google_event_htmllink',)


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
                  'modified', 'google_calendar_published', 'google_event_id',
                  'google_event_htmllink')

        read_only_fields = 'created', 'modified', 'google_event_id', \
                           'google_event_htmllink', 'status'

    def create(self, validated_data):
        if validated_data.get('google_calendar_published') is True:
            event_id, html_link = self.create_google_calendar_event(
                validated_data)
            if event_id:
                validated_data['google_event_id'] = event_id
                validated_data['google_event_htmllink'] = html_link
                validated_data['status'] = 'published'
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('google_calendar_published') is True and \
                not instance.google_event_id:
            event_id, html_link = self.create_google_calendar_event(
                validated_data)
            if event_id:
                instance.google_event_id = event_id
                instance.google_event_htmllink = html_link
                instance.status = 'published'
        elif validated_data.get('google_calendar_published') is True and \
                instance.google_event_id:
            self.update_google_calendar_event(instance.google_event_id,
                                              validated_data)
        elif validated_data.get('google_calendar_published') is False and\
                instance.google_event_id:
            if self.remove_google_calendar_event(
                        instance.google_event_id):
                instance.google_event_id = None
                instance.google_event_htmllink = None
                instance.status = 'draft'
            else:
                raise serializers.ValidationError(
                    _('There was an error removing from calendar'))
        return super().update(instance, validated_data)

    def save(self):
        user = self.context.get("request").user \
            if 'request' in self.context else None
        self.validated_data['user'] = user

        return super().save()

    def create_google_calendar_event(self, data):
        """
        Create event in Google Calendar
        """
        # TODO Refactor to celery
        gcalendar = services.GoogleCalendarService()
        gcalendar.initialize()

        event = {
            'summary': f'{data.get("group")} - {data.get("title")}',
            'location': data.get('location'),
            'description': data.get('description'),
            'start': {
                'dateTime': data.get('start').isoformat(),
            },
            'end': {
                'dateTime': data.get('end').isoformat(),
            },
        }

        created_event = gcalendar.create_event(event)
        event_id = created_event.get('id')
        event_htmllink = created_event.get('htmlLink')

        return event_id, event_htmllink

    def update_google_calendar_event(self, event_id, data):
        """
        Update event in Google Calendar
        """
        # TODO Refactor to celery
        gcalendar = services.GoogleCalendarService()
        gcalendar.initialize()

        event = {
            'summary': f'{data.get("group")} - {data.get("title")}',
            'location': data.get('location'),
            'description': data.get('description'),
            'start': {
                'dateTime': data.get('start').isoformat(),
            },
            'end': {
                'dateTime': data.get('end').isoformat(),
            },
        }

        updated_event = gcalendar.update_event(event_id, event)
        event_id = updated_event.get('id')
        event_htmllink = updated_event.get('htmlLink')

        return event_id, event_htmllink

    def remove_google_calendar_event(self, event_id):
        """
        Delete event in Google Calendar
        """
        # TODO Refactor to celery
        gcalendar = services.GoogleCalendarService()
        gcalendar.initialize()

        try:
            gcalendar.delete_event(event_id)
        except services.GoogleCalendarError:
            return False
        return True

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
        data['end'] = data.get('start') + timedelta(minutes=duration)

        return data
