import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)

notes = {}

"""Adds note to the dictionary. When a note is created uuid and time_created should be generated."""
@app.route('/api/note', methods=['POST'])
def create_note():
    request_note = request.get_json()
    id=uuid.uuid4().int


    note={id:request_note}

    notes.update(note)
    print(notes)


    return jsonify(notes)







"List all stored notes."
@app.route('/api/note')
def get_notes():
    return jsonify(notes)


# @app.route('/api/note/<uuid>')
# "Retrieve a single note"
#
# @app.route('/api/note/<uuid>', methods=['PATCH'])
# "Updated note with provided uuid. When a note is updated time_updated should be generated."
#
# @app.route('/api/note/<uuid>', methods=['DELETE'])
# "Deletes note with provided uuid."


app.run(debug=True)
