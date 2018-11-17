import datetime

from django.conf import settings

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleCalendarError(HttpError):
    pass


class GoogleCalendarService:
    def __init__(self, calendar_id=None, calendar_credentials=None):
        if not calendar_id:
            calendar_id = settings.GOOGLE_CALENDAR_ID
        if not calendar_credentials:
            calendar_credentials = settings.GOOGLE_CALENDAR_CREDENTIALS
        self.service = None
        self.calendarId = calendar_id
        self.calendarCredentials = calendar_credentials

        self.initialize()

    def initialize(self):
        creds = service_account.Credentials.from_service_account_file(
            self.calendarCredentials)
        scoped_credentials = creds.with_scopes(
            ['https://www.googleapis.com/auth/calendar'])

        self.service = build('calendar', 'v3',
                             credentials=scoped_credentials)

    def create_event(self, event_data):
        return self.service.events().insert(
            calendarId=self.calendarId,
            body=event_data).execute()

    def update_event(self, event_id, event_data):
        return self.service.events().update(
            calendarId=self.calendarId, eventId=event_id,
            body=event_data).execute()

    def delete_event(self, event_id):
        return self.service.events().delete(
            calendarId=settings.GOOGLE_CALENDAR_ID,
            eventId=event_id).execute()

    def get_calendar(self):
        return self.service.calendarList().get(
            calendarId=self.calendarId).execute()

    def list_events(self, time_min=None, time_max=None):
        if not time_max:
            dt = datetime.datetime.now() + datetime.timedelta(weeks=4)
            time_max = dt.strftime("%Y-%m-%dT%H:%M:%SZ")

        events = self.service.events().list(calendarId=self.calendarId,
                                            singleEvents=True,
                                            orderBy='startTime',
                                            timeMin=time_min,
                                            timeMax=time_max).execute()
        return events.get('items', [])
