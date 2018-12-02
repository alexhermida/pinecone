import requests

from django.core.management.base import BaseCommand
from django.utils.translation import gettext as _

from api import serializers


class Command(BaseCommand):
    help = 'Synchronice groups from public json'

    def add_arguments(self, parser):
        parser.add_argument('url_members', help=_('External url for '
                                                    'importing members'))

    def handle(self, *args, **options):
        url = options['url_members']

        print('Syncing groups...')
        response = requests.get(url).json()

        for name, val in response['members'].items():
            serializer = serializers.GroupSerializer(data=val)

            if not serializer.is_valid():
                print('Validation error:', serializer.errors['name'][0])
                continue

            serializer.save()
