import datetime
import uuid
from http.client import BAD_REQUEST
from marshmallow import Schema, fields, validates, ValidationError
from flask import Flask, request
from marshmallow.validate import Length, Range
from werkzeug.exceptions import abort

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
    errors = create_note_schema.validate(request.get_json())
    if errors:
        abort(BAD_REQUEST, str(errors))
    current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    time_created = {"time_created": current_time}
    request_note = request.get_json()
    request_note.update(time_created)
    note = {uuid.uuid4().int: request_note}
    notes.update(note)
    return note


@app.route('/api/note')
def get_notes():
    return notes


@app.route('/api/note/<int:uid>')
def get_note(uid):
    note = notes[uid]
    return note


@app.route('/api/note/<int:uid>', methods=['PATCH'])
def update_note(uid):
    errors = update_note_schema.validate(request.get_json())
    if errors:
        abort(BAD_REQUEST, str(errors))
    request_update = request.get_json()
    notes[uid].update(request_update)
    note = notes[uid]
    current_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    time_updated = {"time_updated": current_time}
    note.update(time_updated)
    return note


@app.route('/api/note/<int:uid>', methods=['DELETE'])
def delete_note(uid):
    note = notes.pop(uid)
    return note


app.run(debug=True)
