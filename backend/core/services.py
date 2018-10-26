from django.conf import settings

import httplib2
from googleapiclient.discovery import build
from google.oauth2 import service_account


class GoogleCalendarService:
    def __init__(self):
        self.service = None
        self.calendarId = settings.GOOGLE_CALENDAR_ID

        self.initialize()

    def initialize(self):
        creds = service_account.Credentials.from_service_account_file(
            settings.GOOGLE_CALENDAR_CREDENTIAL)
        scoped_credentials = creds.with_scopes(
            ['https://www.googleapis.com/auth/calendar'])

        self.service = build('calendar', 'v3',
                             http=scoped_credentials.authorize(httplib2.Http()))

    def create_event(self, event_data):
        return self.service.events().insert(
            calendarId=self.calendarId,
            body=event_data).execute()

    def delete_event(self, event_id):
        return self.service.events().delete(
            calendarId=settings.GOOGLE_CALENDAR_ID,
            eventId=event_id).execute()

    def get_calendar(self):
        return self.service.calendarList().get(
            calendarId=self.calendarId).execute()

    def list_events(self):
        events = self.service.events().list(calendarId=self.calendarId,
                                            singleEvents=True,
                                            orderBy='startTime').execute()
        return events.get('items', [])
