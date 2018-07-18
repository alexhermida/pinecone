import datetime as dt

import pytest

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
