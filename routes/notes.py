from core import db, init_app
from flask import request, jsonify
from core.models import Notes
from pydantic import ValidationError
from flask_restx import Api, Resource
from schemas.note_schemas import NoteValidator
import json
from core.middleware import authorize_user

app = init_app()
api = Api(app=app, prefix='/api')

@api.route("/notes")
class NotesApi(Resource):

    method_decorators =(authorize_user,)

    def post(self, *args, **kwargs):
        try:
            serializer = NoteValidator(**request.get_json())
            note = Notes(**serializer.model_dump())
            db.session.add(note)
            db.session.commit()
            return {"message": "Note added successfully", 'status': 201, 'data': note.json}, 201
        except ValidationError as e:
            err = json.loads(e.json())
            return {'message': f'{err[0]["input"]}-{err[0]["msg"]}', "status": 400}, 400
        except Exception as e:
            return {'message': 'Something went wrong','status': 500}, 500

    def get(self, *args, **kwargs):
        try:
            print(kwargs)
            user_id = kwargs.get('user_id')
            if not user_id:
                return {'message': 'User ID not provided','status': 400}, 400

            notes = Notes.query.filter_by(user_id=user_id).all()
            if notes:
                return {"message": " Notes found","status":200,"data": [note.json for note in notes]},200 #change status code
            return {"message": "Notes not found",'status': 404},404 # change status code
        except Exception as e:
            return {'message': 'Something went wrong','status':500}, 500
        
    def put(self, *args, **kwargs):
        try:
            data = request.json
            note = Notes.query.filter_by(id=data['id'], user_id=data['user_id']).first()
            if not note:
                return {"message": "Note not found","status": 404}, 404

            serializer = NoteValidator(**request.get_json())
            updated_data = serializer.model_dump()
            [setattr(note, key, value) for key, value in updated_data.items()]
            db.session.commit()
            return {"message": "Note updated successfully","status":200,"data":note.json}, 200
        except ValidationError as e:
            err = json.loads(e.json())
            return {'message': f'{err[0]["input"]}-{err[0]["msg"]}', "status": 400}, 400
        except Exception as e:
            return {'message': 'Something went wrong',"status": 500}, 500


@api.route("/notes/<int:id>")
class NoteApi(Resource):

    method_decorators = (authorize_user,)

    def get(self, *args, **kwargs):
        try:
            print(kwargs)
            note = Notes.query.filter_by(**kwargs).first()
            if note:
                return { "message": "Notes found","status":200,"data":note.json},200 #change status code
            return {"message": "Note not found", "status" : 404 }, 404
        except Exception as e:
            return {'message': 'Something went wrong', "status": 500}, 500

    def delete(self, *args, **kwargs):
        try:
            note = Notes.query.filter_by(**kwargs).first()
            if not note:
                return {"message": "Note not found", "status" :404}, 404

            db.session.delete(note)
            db.session.commit()
            return {"message": "Note deleted successfully", "status" :204}, 204
        except Exception as e:
            return {'message': 'Something went wrong',"status": 500}, 500
