import pytest


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
