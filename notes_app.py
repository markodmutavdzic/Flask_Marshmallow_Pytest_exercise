import datetime
import uuid
from http.client import BAD_REQUEST

from marshmallow import Schema, fields, validates, ValidationError
from flask import Flask, request
from marshmallow.validate import Length, Range

app = Flask(__name__)

notes = {}


class CreateNoteInput(Schema):
    title = fields.Str(required=True, validate=Length(max=20))
    note = fields.Str(required=True, validate=Length(max=100))
    user_id = fields.Int(required=True, validate=Range(min=0))

    @validates('note')
    def contains_forbidden_word(self, text):
        forbidden_words = ['unbelievable', 'impossible', 'undoable', 'can not', 'would not']
        for word in forbidden_words:
            if word in text.lower():
                raise ValidationError("Note contains forbidden word")


class UpdateNoteInput(Schema):
    title = fields.Str(required=False, validate=Length(max=20))
    note = fields.Str(required=False, validate=Length(max=100))
    user_id = fields.Int(required=False, validate=Range(min=0))
    time_created = fields.Str(required=False)
    time_updated = fields.Str(required=False)

    @validates('note')
    def contains_forbidden_word(self, text):
        forbidden_words = ['unbelievable', 'impossible', 'undoable', 'can not', 'would not']
        for word in forbidden_words:
            if word in text.lower():
                raise ValidationError("Note contains forbidden word")


create_note_schema = CreateNoteInput()
update_note_schema = UpdateNoteInput()


@app.route('/api/note', methods=['POST'])
def create_note():
    try:
        input_data = create_note_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, BAD_REQUEST

    current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    time_created = {"time_created": current_time}
    note = {str(uuid.uuid4()): {**input_data, **time_created}}
    notes.update(note)
    return note


@app.route('/api/note')
def get_notes():
    return notes


@app.route('/api/note/<string:uid>')
def get_note(uid):
    note = notes.get(uid)
    if not note:
        return 'Note does not exist', BAD_REQUEST
    return note


@app.route('/api/note/<string:uid>', methods=['PATCH'])
def update_note(uid):

    try:
        input_data = update_note_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, BAD_REQUEST

    note = notes.get(uid)
    if not note:
        return "Note does not exist", BAD_REQUEST

    current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    time_updated = {"time_updated": current_time}
    note.update(**input_data, **time_updated)
    return note


@app.route('/api/note/<string:uid>', methods=['DELETE'])
def delete_note(uid):
    note = notes.get(uid)
    if not note:
        return "Note does not exist", BAD_REQUEST
    notes.pop(uid)
    return note


app.run()
