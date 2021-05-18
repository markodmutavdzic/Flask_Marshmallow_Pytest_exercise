from unittest.mock import patch
from freezegun import freeze_time
import pytest
from notes import app, notes


@pytest.fixture()
def client():
    client = app.test_client()
    return client


def test_get_notes_empty(client):
    response = client.get('/api/note')
    assert response.get_json() == {}


@freeze_time('18-05-2021 15:42:50')
def test_create_note(client):
    with patch("notes.uuid.uuid4") as uuid:
        uuid.return_value = 123
        data = {
            "title": "Poruka",
            "note": "Ovo je poruka",
            "user_id": 123
            }
        url = '/api/note'
        response = client.post(url, json=data)
    expected_result = {'123': {'note': 'Ovo je poruka',
                             'time_created': '18-05-2021 15:42:50',
                             'title': 'Poruka',
                             'user_id': 123}}
    assert response.get_json() == expected_result


def test_get_notes_with_123_note(client):
    response = client.get('/api/note')
    expected_result = {'123': {'note': 'Ovo je poruka',
                             'time_created': '18-05-2021 15:42:50',
                             'title': 'Poruka',
                             'user_id': 123}}
    assert response.get_json() == expected_result


def test_get_note(client):
    response = client.get('/api/note/123')
    expected_result = {'note': 'Ovo je poruka',
                               'time_created': '18-05-2021 15:42:50',
                               'title': 'Poruka',
                               'user_id': 123}
    assert response.get_json() == expected_result


@freeze_time('18-05-2021 15:50:50')
def test_update_note(client):
    data = {
        "note": "Ovo je patch poruka",
        }
    url = '/api/note/123'
    expected_result = {'note': 'Ovo je patch poruka',
                         'time_created': '18-05-2021 15:42:50',
                         'time_updated': '18-05-2021 15:50:50',
                         'title': 'Poruka',
                         'user_id': 123}
    response = client.patch(url, json=data)
    assert response.get_json() == expected_result


@freeze_time('18-05-2021 15:51:50')
def test_update_note_second_time(client):
    data = {
        "note": "Ovo je druga patch poruka",
        }
    url = '/api/note/123'
    expected_result = {'note': 'Ovo je druga patch poruka',
                         'time_created': '18-05-2021 15:42:50',
                         'time_updated': '18-05-2021 15:51:50',
                         'title': 'Poruka',
                         'user_id': 123}
    response = client.patch(url, json=data)
    assert response.get_json() == expected_result


def test_delete_note(client):
    response = client.delete('/api/note/123')
    expected_result = {'note': 'Ovo je druga patch poruka',
                       'time_created': '18-05-2021 15:42:50',
                       'time_updated': '18-05-2021 15:51:50',
                       'title': 'Poruka',
                       'user_id': 123}
    assert response.get_json() == expected_result


