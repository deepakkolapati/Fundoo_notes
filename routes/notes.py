from core import db, init_app
from flask import request, jsonify
from core.models import Notes
from pydantic import ValidationError
from flask_restx import Api, Resource
from schemas.note_schemas import NoteValidator
import json

app = init_app()
api = Api(app=app, prefix='/api')

@api.route("/notes")
class NotesApi(Resource):
    def post(self):
        try:
            serializer = NoteValidator(**request.get_json())
            note = Notes(**serializer.model_dump())
            db.session.add(note)
            db.session.commit()
            return {"message": "Note added successfully", "id": note.id}, 201
        except ValidationError as e:
            err = json.loads(e.json())
            return {'message': f'{err[0]["input"]}-{err[0]["msg"]}', "status": 400}, 400
        except Exception as e:
            return {'message': 'Something went wrong'}, 500

    def get(self):
        try:
            user_id = request.args.get('user_id')
            if not user_id:
                return {'message': 'User ID not provided'}, 400

            notes = Notes.query.filter_by(user_id=int(user_id)).all()
            if notes:
                return {"notes": [note.json for note in notes]}
            return {"message": "Notes not found"}
        except Exception as e:
            return {'message': 'Something went wrong'}, 500

@api.route("/notes/<int:note_id>")
class NoteApi(Resource):
    def get(self, note_id):
        try:
            note = Notes.query.get(note_id)
            if note:
                return note.json
            return {"message": "Note not found"}, 404
        except Exception as e:
            return {'message': 'Something went wrong'}, 500

    def put(self, note_id):
        try:
            note = Notes.query.get(note_id)
            if not note:
                return {"message": "Note not found"}, 404

            serializer = NoteValidator(**request.get_json())
            updated_data = serializer.model_dump()
            for key, value in updated_data.items():
                setattr(note, key, value)

            db.session.commit()
            return {"message": "Note updated successfully"}, 200
        except ValidationError as e:
            err = json.loads(e.json())
            return {'message': f'{err[0]["input"]}-{err[0]["msg"]}', "status": 400}, 400
        except Exception as e:
            return {'message': 'Something went wrong'}, 500

    def delete(self, note_id):
        try:
            note = Notes.query.get(note_id)
            if not note:
                return {"message": "Note not found"}, 404

            db.session.delete(note)
            db.session.commit()
            return {"message": "Note deleted successfully"}, 204
        except Exception as e:
            return {'message': 'Something went wrong'}, 500
