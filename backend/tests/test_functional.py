import datetime as dt
from unittest.mock import patch

import pytest

from django.utils.timezone import make_aware
from django.utils.translation import gettext as _

from core import factories


@pytest.mark.django_db
def test_admin(client):
    response = client.get('/admin/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_unauthenticated(client):
    response = client.get('/api/')
    assert response.status_code == 401


def test_authenticated(admin_client):
    response = admin_client.get('/api/')
    assert response.status_code == 200


def test_get_open_closest_events(admin_client):
    start_date = make_aware(dt.datetime(2017, 1, 1, 10))

    [factories.EventFactory(start=start_date) for _ in
     range(0, 10)]

    future_start_date = make_aware(dt.datetime(2100, 1, 1, 8))
    factories.EventFactory(start=future_start_date)

    response = admin_client.get('/api/events-closests/')

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['start'] == future_start_date.strftime(
        '%Y-%m-%dT%H:%M:%SZ')


def test_get_events_descendent_order(admin_client):
    [factories.EventFactory() for _ in range(0, 10)]

    response = admin_client.get('/api/events/')

    assert response.status_code == 200
    assert len(response.json()) == 10
    assert response.json()[0]['id'] == 21


def test_create_event_with_required_fields(admin_client):
    group = factories.GroupFactory()

    data = {'description': 'descrición evento test',
            'group': group.id}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 201


def test_create_draft_event(admin_client):
    group = factories.GroupFactory()

    data = {'description': 'descrición evento test',
            'group': group.id}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 201
    assert response.json()['status'] == 'draft'


def test_update_draft_event(admin_client):
    event = factories.EventFactory(description='My test event')
    data = {'description': 'new description'}
    response = admin_client.patch(f'/api/events/{event.id}/', data,
                                  content_type='application/json')
    assert response.status_code == 200
    assert response.json()['description'] == 'new description'


@patch('api.serializers.EventCreateSerializer.create_google_calendar_event',
       lambda x, y: (101, 'http://test.local'))
def test_publish_created_event(admin_client):
    start_date = make_aware(dt.datetime(2030, 1, 1, 10))
    event = factories.EventFactory(description='Event to publish',
                                   status='draft')
    assert event.status == 'draft'

    data = {'start': start_date,
            'duration': 2, 'google_calendar_published': True}
    response = admin_client.patch(f'/api/events/{event.id}/', data,
                                  content_type='application/json')
    assert response.status_code == 200
    assert response.json()['google_calendar_published'] is True
    assert response.json()['status'] == 'published'

    response = admin_client.get(f'/api/events/{event.id}/')
    assert response.json()['status'] == 'published'
    assert response.json()['google_event_id'] == '101'


@patch('api.serializers.EventCreateSerializer.create_google_calendar_event',
       lambda x, y: (101, 'http://test.local'))
def test_create_published_event(admin_client):
    group = factories.GroupFactory()

    start_date = make_aware(dt.datetime(2030, 1, 1, 10))
    data = {'description': 'descrición evento test',
            'group': group.id, 'start': start_date,
            'duration': 2, 'google_calendar_published': True}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 201
    assert response.json()['status'] == 'published'
    assert response.json()['google_event_id'] == '101'


@patch('api.serializers.EventCreateSerializer.remove_google_calendar_event',
       lambda x, y: True)
def test_remove_published_event(admin_client):
    group = factories.GroupFactory()
    start_date = make_aware(dt.datetime(2030, 1, 1, 10))
    data = {'description': 'descrición evento test',
            'group': group, 'start': start_date,
            'duration': 2, 'google_calendar_published': True,
            'google_event_id': 102,
            'google_event_htmllink': 'http://test.local',
            'status': 'published'}
    event = factories.EventFactory(**data)

    response = admin_client.get(f'/api/events/{event.id}/')
    assert response.json()['status'] == 'published'
    assert response.json()['google_calendar_published'] is True

    data = {'google_calendar_published': False}
    response = admin_client.patch(f'/api/events/{event.id}/', data,
                                  content_type='application/json')

    assert response.status_code == 200
    assert response.json()['google_calendar_published'] is False
    assert response.json()['status'] == 'draft'
    assert response.json()['google_event_id'] is None
    assert response.json()['google_event_htmllink'] is None


@patch('api.serializers.EventCreateSerializer.create_google_calendar_event',
       lambda x, y: (101, 'http://test.local'))
def test_update_published_event(admin_client):
    group = factories.GroupFactory()
    start_date = make_aware(dt.datetime(2030, 1, 1, 10))
    duration = 120
    end_date = start_date + dt.timedelta(minutes=duration)
    data = {'description': 'descrición evento test',
            'group': group, 'start': start_date,
            'duration': duration,
            'end': end_date,
            'google_calendar_published': True,
            'google_event_id': 102,
            'google_event_htmllink': 'http://test.local',
            'status': 'published'}
    event = factories.EventFactory(**data)
    assert event.status == 'published'

    new_start_date = make_aware(dt.datetime(2030, 1, 1, 11))
    data = {'start': new_start_date, 'duration': duration}
    response = admin_client.patch(f'/api/events/{event.id}/', data,
                                  content_type='application/json')

    assert response.status_code == 200
    assert response.json()['google_calendar_published'] is True
    assert response.json()['start'] == \
        new_start_date.strftime('%Y-%m-%dT%H:%M:%SZ')


def test_prevent_create_event_without_description(admin_client):
    group = factories.GroupFactory()
    data = {'group': group.id}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 400


def test_prevent_create_event_without_group(admin_client):
    data = {'description': 'descrición evento test'}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 400
    assert 'group' in response.json()


def test_prevent_create_event_with_only_start_date(admin_client):
    group = factories.GroupFactory()
    start_date = make_aware(dt.datetime(2019, 1, 1, 10))
    data = {'group': group.id, 'description': 'descrición evento test',
            'start': start_date}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 400
    assert response.json()['non_field_errors'] == [
        _('If you enter start date you must enter the duration')]


def test_prevent_publish_gcal_event_without_dates(admin_client):
    group = factories.GroupFactory()

    data = {'description': 'descrición evento test',
            'group': group.id,
            'google_calendar_published': True}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 400
    assert response.json()['non_field_errors'] == [
        _('To publish in Google Calendar you must enter start '
          'time and duration')]


def test_prevent_publish_gcal_event_without_start_date(admin_client):
    group = factories.GroupFactory()
    data = {'description': 'descrición evento test',
            'group': group.id, 'end': dt.datetime.now(),
            'google_calendar_published': True}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 400
    assert response.json()['non_field_errors'] == [
        _('To publish in Google Calendar you must enter start '
          'time and duration')]


def test_prevent_publish_gcal_event_without_duration(admin_client):
    group = factories.GroupFactory()
    data = {'description': 'descrición evento test',
            'group': group.id, 'end': dt.datetime.now(),
            'google_calendar_published': True}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 400
    assert response.json()['non_field_errors'] == [
        _('To publish in Google Calendar you must enter start '
          'time and duration')]
