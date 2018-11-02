import datetime as dt

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
    data = {'description': 'descrición evento test',
            'group': 'VigoTechGroup'}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 201


def test_prevent_create_event_without_description(admin_client):
    data = {'group': 'VigoTechGroup'}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 400


def test_prevent_create_event_without_group(admin_client):
    data = {'description': 'descrición evento test'}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 400
    assert 'group' in response.json()


def test_prevent_create_event_with_only_start_date(admin_client):
    start_date = make_aware(dt.datetime(2019, 1, 1, 10))
    data = {'group': 'VigoTechGroup', 'description': 'descrición evento test',
            'start': start_date}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 400
    assert response.json()['non_field_errors'] == [
        _('If you enter start date you must enter the end date')]


def test_prevent_publish_gcal_event_without_dates(admin_client):
    data = {'description': 'descrición evento test',
            'group': 'VigoTechGroup',
            'google_calendar_published': True}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 400
    assert response.json()['non_field_errors'] == [
        _('To publish in Google Calendar you must enter start/end '
          'datetime and update the status')]


def test_prevent_publish_gcal_event_without_start_date(admin_client):
    data = {'description': 'descrición evento test',
            'group': 'VigoTechGroup', 'end': dt.datetime.now(),
            'google_calendar_published': True}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 400
    assert response.json()['non_field_errors'] == [
        _('To publish in Google Calendar you must enter start/end '
          'datetime and update the status')]


def test_prevent_publish_gcal_event_without_end_date(admin_client):
    data = {'description': 'descrición evento test',
            'group': 'VigoTechGroup', 'end': dt.datetime.now(),
            'google_calendar_published': True}
    response = admin_client.post('/api/events/', data)

    assert response.status_code == 400
    assert response.json()['non_field_errors'] == [
        _('To publish in Google Calendar you must enter start/end '
          'datetime and update the status')]
