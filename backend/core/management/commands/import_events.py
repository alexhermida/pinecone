import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from core import models, services

from api import serializers


def get_group(text):
    for group in models.Group.objects.all():
        if group.name in text:
            return group.id


class Command(BaseCommand):
    help = 'Simple task to import events from a Google Calendar'

    def add_arguments(self, parser):
        parser.add_argument('--calendar_id', required=True)
        parser.add_argument('--credentials_path', required=True)
        parser.add_argument('--from_date', help=_(
            "Add first date in format: 2018-11-01T00:00:00Z"), required=True)
        parser.add_argument('--to_date', help=_(
            "Add last date in format: 2018-11-01T00:00:00Z"), required=True)
        parser.add_argument('--publish', action='store_true',
                            help=_("Publish in destination calendar"),
                            required=True)

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(
                self.style.WARNING('Running in production! Command disabled'))
            return

        calendar_id = options['calendar_id']
        credentials_path = options['credentials_path']
        time_min = options['from_date']
        time_max = options['to_date']
        publish = options['publish']

        print('Importing events...')

        gcalendar = services.GoogleCalendarService(
            calendar_id=calendar_id,
            calendar_credentials=credentials_path)
        gcalendar.initialize()

        for event in gcalendar.list_events(time_min, time_max):
            start_date = event.get('start').get('dateTime') if event.get(
                'start').get('dateTime') else event.get('start').get('date')
            end_date = event.get('end').get('dateTime') if event.get(
                'end').get('dateTime') else event.get('end').get('date')

            dt_start = datetime.datetime.fromisoformat(start_date)
            dt_end = datetime.datetime.fromisoformat(end_date)
            start = dt_start
            duration = (dt_end - dt_start).total_seconds() / 60

            data = {
                'title': event.get('summary'),
                'description': event.get('description') if event.get(
                    'description') else event.get('summary'),
                'group': get_group(event.get('summary')),
                'start': start,
                'duration': duration,
                'google_calendar_published': publish,
                'import_id': event.get('id'),
            }
            print(data, '\n')

            serializer = serializers.EventCreateSerializer(data=data)

            if not serializer.is_valid():
                print('Validation error:', serializer.errors)
                continue

            serializer.save()
