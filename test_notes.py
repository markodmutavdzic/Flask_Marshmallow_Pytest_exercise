from unittest.mock import patch
from freezegun import freeze_time
import pytest

from notes import app


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


# u narednih nekoliko testova nisam koristio freeze_time i patch uuid-a jer ionako prekida izvrsenje jer ne prolazi
# validaciju
def test_create_note_with_invalid_input_no_title(client):
    data = {

        "note": "Ovo je poruka",
        "user_id": 123
    }
    url = '/api/note'
    response = client.post(url, json=data)
    assert response.status_code == 400


def test_create_note_with_invalid_input_title_too_long(client):
    data = {
        "title": "Poruka 123456890123456789",
        "note": "Ovo je poruka",
        "user_id": 123
    }
    url = '/api/note'
    response = client.post(url, json=data)
    assert response.status_code == 400


def test_create_note_with_invalid_input_no_note(client):
    data = {
        "title": "Poruka",

        "user_id": 123
    }
    url = '/api/note'
    response = client.post(url, json=data)
    assert response.status_code == 400


def test_create_note_with_invalid_input_note_too_long(client):
    data = {
        "title": "Poruka",
        "note": "Ovo je poruka 567892123456789312345678941234567895123456789612345678971234567898123456789912345689100",
        "user_id": 123
    }
    url = '/api/note'
    response = client.post(url, json=data)
    assert response.status_code == 400


# ovaj test sam prvo mislio da uradim paramerizacijom pa mi je bio komplikovano, onda sam improvizovao
def test_create_note_with_invalid_input_note_contains_forbidden_words(client):
    forbidden_words = ['unbelievable', 'impossible', 'undoable', 'can not', 'would not']
    for word in forbidden_words:
        data = {
            "title": "Poruka",
            "note": f"Ovo je poruka{word} ",
            "user_id": 123
        }
        url = '/api/note'
        response = client.post(url, json=data)
        assert response.status_code == 400


def test_create_note_with_invalid_input_no_user_id(client):
    data = {
        "title": "Poruka",
        "note": "Ovo je poruka",

    }
    url = '/api/note'
    response = client.post(url, json=data)
    assert response.status_code == 400


def test_create_note_with_invalid_input_user_id_out_of_range(client):
    data = {
        "title": "Poruka",
        "note": "Ovo je poruka",
        "user_id": -123
    }
    url = '/api/note'
    response = client.post(url, json=data)
    assert response.status_code == 400


def test_get_notes_with_123_note(client):
    response = client.get('/api/note')
    expected_result = {'123': {'note': 'Ovo je poruka',
                               'time_created': '18-05-2021 15:42:50',
                               'title': 'Poruka',
                               'user_id': 123}}
    assert response.get_json() == expected_result


def test_get_note_123(client):
    response = client.get('/api/note/123')
    expected_result = {'note': 'Ovo je poruka',
                       'time_created': '18-05-2021 15:42:50',
                       'title': 'Poruka',
                       'user_id': 123}
    assert response.get_json() == expected_result


def test_get_note_with_non_existent_note(client):
    response = client.get('/api/note/456')
    assert response.status_code == 400


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


def test_update_note_with_invalid_input_title_too_long(client):
    data = {
        "title": "Poruka 123456890123456789",
        "note": "Ovo je poruka",
        "user_id": 123
    }
    url = '/api/note'
    response = client.patch(url, json=data)
    assert response.status_code == 405


def test_update_note_with_invalid_input_note_too_long(client):
    data = {
        "title": "Poruka",
        "note": "Ovo je poruka 567892123456789312345678941234567895123456789612345678971234567898123456789912345689100",
        "user_id": 123
    }
    url = '/api/note'
    response = client.patch(url, json=data)
    assert response.status_code == 405


def test_update_note_with_invalid_input_user_id_out_of_range(client):
    data = {
        "title": "Poruka",
        "note": "Ovo je poruka",
        "user_id": -123
    }
    url = '/api/note'
    response = client.patch(url, json=data)
    assert response.status_code == 405


def test_update_note_with_invalid_input_note_contains_forbidden_words(client):
    forbidden_words = ['unbelievable', 'impossible', 'undoable', 'can not', 'would not']
    for word in forbidden_words:
        data = {
            "title": "Poruka",
            "note": f"Ovo je poruka {word} ",
            "user_id": 123
        }
        url = '/api/note'
        response = client.patch(url, json=data)
        assert response.status_code == 405


def test_delete_note(client):
    response = client.delete('/api/note/123')
    expected_result = {'note': 'Ovo je druga patch poruka',
                       'time_created': '18-05-2021 15:42:50',
                       'time_updated': '18-05-2021 15:51:50',
                       'title': 'Poruka',
                       'user_id': 123}
    assert response.get_json() == expected_result


def test_delete_note_with_non_existent_note(client):
    response = client.delete('/api/note/465')
    assert response.status_code == 400
