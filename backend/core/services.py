from django.conf import settings

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


class GoogleCalendarService:
    def __init__(self):
        self.service = None
        self.calendarId = settings.GOOGLE_CALENDAR_ID

        self.initialize()

    def initialize(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            settings.GOOGLE_CALENDAR_CREDENTIALS,
            scopes=['https://www.googleapis.com/auth/calendar'])

        self.service = build('calendar', 'v3',
                             http=creds.authorize(httplib2.Http()))

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
