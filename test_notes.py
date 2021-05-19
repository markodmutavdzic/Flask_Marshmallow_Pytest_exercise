from unittest.mock import patch
from freezegun import freeze_time
import pytest
from notes_app import app


@pytest.fixture()
def client():
    client = app.test_client()
    return client


@pytest.fixture()
def notes_for_test_empty():
    return {}


@pytest.fixture()
def notes_for_test_123():
    return {'123' : {'note': 'Ovo je poruka',
                     'time_created': '18-05-2021 15:42:50',
                     'title': 'Poruka',
                     'user_id': 123}}


def test_get_notes_empty(client, notes_for_test_empty):
    with patch.dict('notes_app.notes',notes_for_test_empty):
        response = client.get('/api/note')

        assert response.status_code == 200
        assert response.get_json() == {}


@freeze_time('18-05-2021 15:42:50')
def test_create_note(client, notes_for_test_empty):
    with patch.dict('notes_app.notes', notes_for_test_empty):
        with patch("notes_app.uuid.uuid4") as uuid:
            uuid.return_value = 123
            data = {
                "title": "Poruka",
                "note": "Ovo je poruka",
                "user_id": 123
            }
            url = '/api/note'
            response = client.post(url, json=data)

        assert response.status_code == 200
        assert response.get_json() == {'123': {'note': 'Ovo je poruka',
                                       'time_created': '18-05-2021 15:42:50',
                                       'title': 'Poruka',
                                       'user_id': 123}}


def test_create_note_with_invalid_input_no_title(client):
    data = {

        "note": "Ovo je poruka",
        "user_id": 123
    }
    url = '/api/note'
    response = client.post(url, json=data)

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


def test_create_note_with_invalid_input_title_too_long(client):
    data = {
        "title": "Poruka"*5,
        "note": "Ovo je poruka",
        "user_id": 123
    }
    url = '/api/note'
    response = client.post(url, json=data)

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


def test_create_note_with_invalid_input_no_note(client):
    data = {
        "title": "Poruka",

        "user_id": 123
    }
    url = '/api/note'
    response = client.post(url, json=data)

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


def test_create_note_with_invalid_input_note_too_long(client):
    data = {
        "title": "Poruka",
        "note": "Ovo je poruka"*10,
        "user_id": 123
    }
    url = '/api/note'
    response = client.post(url, json=data)

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


def test_create_note_with_invalid_input_note_contains_forbidden_word_unbelievable(client):
    data = {
        "title": "Poruka",
        "note": "Ovo je poruka unbelievable ",
        "user_id": 123
    }
    url = '/api/note'
    response = client.post(url, json=data)

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


def test_create_note_with_invalid_input_note_contains_forbidden_word_undoable(client):
    data = {
        "title": "Poruka",
        "note": "Ovo je poruka undoable ",
        "user_id": 123
    }
    url = '/api/note'
    response = client.post(url, json=data)

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


def test_create_note_with_invalid_input_no_user_id(client):
    data = {
        "title": "Poruka",
        "note": "Ovo je poruka",

    }
    url = '/api/note'
    response = client.post(url, json=data)

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


def test_create_note_with_invalid_input_user_id_out_of_range(client):
    data = {
        "title": "Poruka",
        "note": "Ovo je poruka",
        "user_id": -123
    }
    url = '/api/note'
    response = client.post(url, json=data)

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


def test_get_notes_with_123_note(client, notes_for_test_123):
    with patch.dict('notes_app.notes', notes_for_test_123):
        response = client.get('/api/note')

        assert response.status_code == 200
        assert response.get_json() == {'123': {'note': 'Ovo je poruka',
                                                 'time_created': '18-05-2021 15:42:50',
                                                 'title': 'Poruka',
                                                 'user_id': 123}}


def test_get_note_123(client, notes_for_test_123):
    with patch.dict('notes_app.notes', notes_for_test_123):
        response = client.get('/api/note/123')

        assert response.status_code == 200
        assert response.get_json() == {'note': 'Ovo je poruka',
                                       'time_created': '18-05-2021 15:42:50',
                                       'title': 'Poruka',
                                       'user_id': 123}


def test_get_note_with_non_existent_note(client):
    response = client.get('/api/note/456')

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


@freeze_time('18-05-2021 15:50:50')
def test_update_note(client, notes_for_test_123):
    with patch.dict('notes_app.notes', notes_for_test_123):
        data = {
            "note": "Ovo je patch poruka",
        }
        url = '/api/note/123'
        response = client.patch(url, json=data)

        assert response.status_code == 200
        assert response.get_json() == {'note': 'Ovo je patch poruka',
                                       'time_created': '18-05-2021 15:42:50',
                                       'time_updated': '18-05-2021 15:50:50',
                                       'title': 'Poruka',
                                       'user_id': 123}


def test_update_note_with_invalid_input_title_too_long(client):
    data = {
        "title": "Poruka "*5,
        "note": "Ovo je poruka",
        "user_id": 123
    }
    url = '/api/note/123'
    response = client.patch(url, json=data)

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


def test_update_note_with_invalid_input_note_too_long(client):
    data = {
        "title": "Poruka",
        "note": "Ovo je poruka"*10,
        "user_id": 123
    }
    url = '/api/note/123'
    response = client.patch(url, json=data)

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


def test_update_note_with_invalid_input_user_id_out_of_range(client):
    data = {
        "title": "Poruka",
        "note": "Ovo je poruka",
        "user_id": -123
    }
    url = '/api/note/123'
    response = client.patch(url, json=data)

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


def test_update_note_with_invalid_input_note_contains_forbidden_word_unbelievable(client):
    data = {
        "title": "Poruka",
        "note": f"Ovo je poruka unbelievable ",
        "user_id": 123
    }
    url = '/api/note/123'
    response = client.patch(url, json=data)

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


def test_update_note_with_invalid_input_note_contains_forbidden_word_undoable(client):
    data = {
        "title": "Poruka",
        "note": f"Ovo je poruka undoable ",
        "user_id": 123
    }
    url = '/api/note/123'
    response = client.patch(url, json=data)

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'


def test_delete_note(client, notes_for_test_123):
    with patch.dict('notes_app.notes', notes_for_test_123):
        response = client.delete('/api/note/123')

        assert response.status_code == 200
        assert response.get_json() ==  {'note': 'Ovo je poruka',
                                       'time_created': '18-05-2021 15:42:50',
                                       'title': 'Poruka',
                                       'user_id': 123}


def test_delete_note_with_non_existent_note(client):
    response = client.delete('/api/note/465')

    assert response.status_code == 400
    assert str(response) == '<Response streamed [400 BAD REQUEST]>'
