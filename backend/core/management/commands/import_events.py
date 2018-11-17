import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from api import serializers
from core import services


class Command(BaseCommand):
    help = 'Import events from a Google Calendar'

    def add_arguments(self, parser):
        parser.add_argument('--calendar_id')
        parser.add_argument('--credentials_path')
        parser.add_argument('--from_date', help=_("Add first date in format: 2018-11-01T00:00:00Z"))
        parser.add_argument('--to_date', help=_("Add last date in format: 2018-11-01T00:00:00Z"))

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write(
                self.style.WARNING('Running in production! Command disabled'))
            return

        calendar_id = options['calendar_id']
        credentials_path = options['credentials_path']
        time_min = options['from_date']
        time_max = options['to_date']

        print('Importing events...')

        gcalendar = services.GoogleCalendarService(
            calendar_id=calendar_id,
            calendar_credentials=credentials_path)
        gcalendar.initialize()

        for event in gcalendar.list_events(time_min, time_max):
            dt_start = datetime.datetime.fromisoformat(
                event.get('start').get('dateTime'))
            dt_end = datetime.datetime.fromisoformat(
                event.get('end').get('dateTime'))
            start = dt_start
            duration = (dt_end - dt_start).total_seconds() / 60

            print('------------------')
            print('Title:', event.get('summary'))
            print('Description:', event.get('description'))
            print('Start:', event.get('start').get('dateTime'))
            print('gCal link:', event.get('htmlLink'))
            print('------------------')

            data = {
                'title': event.get('summary'),
                'description': event.get('description') if event.get(
                    'description') else event.get('summary'),
                'group': event.get('summary'),
                'start': start,
                'duration': duration,
                'google_calendar_published': False,
                'import_id': event.get('id'),
            }
            serializer = serializers.EventCreateSerializer(data=data)

            if not serializer.is_valid():
                print(serializer.errors)
                continue

            serializer.save()
