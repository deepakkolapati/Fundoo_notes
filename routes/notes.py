from core import db, init_app
from flask import request, jsonify
from core.models import Notes
from pydantic import ValidationError
from flask_restx import Api, Resource
from schemas.note_schemas import NoteValidator
import json
from core.middleware import authorize_user
from core.utils import RedisManager

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
            RedisManager.save(f'user_{note.user_id}',f'note_{note.id}', json.dumps(note.json))
            return {"message": "Note added successfully", 'status': 201, 'data': note.json}, 201
        except ValidationError as e:
            err = json.loads(e.json())
            return {'message': f'{err[0]["input"]}-{err[0]["msg"]}', "status": 400}, 400
        except Exception as e:
            return {'message': 'Something went wrong','status': 500}, 500

    def get(self, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            if not user_id:
                return {'message': 'User ID not provided','status': 400}, 400
            redis_note=RedisManager.get(f'user_{user_id}')
            
            if redis_note:
                return {"message": " Cache Notes Retrieved","status":200,
                        "data": [json.loads(value) for value in redis_note.values()]},200
            notes = Notes.query.filter_by(user_id=user_id).all()
            if notes:
                return {"message": " Notes found","status":200,
                        "data": [note.json for note in notes]},200 
        
            return {"message": "Notes not found",'status': 404},404
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
            RedisManager.save(f'user_{note.user_id}',f'note_{note.id}', json.dumps(note.json))
            return {"message": "Note updated successfully","status":200,"data":note.json}, 200
        except ValidationError as e:
            err = json.loads(e.json())
            return {'message': f'{err[0]["input"]}-{err[0]["msg"]}', "status": 400}, 400
        except Exception as e:
            print(e)
            return {'message': 'Something went wrong',"status": 500}, 500


@api.route("/notes/<int:id>")
class NoteApi(Resource):

    method_decorators = (authorize_user,)

    def get(self, *args, **kwargs):
        try:
            redis_note=RedisManager.get_one(f'user_{kwargs['user_id']}',f'note_{kwargs['id']}')
            if redis_note:
                return { "message": " Cache Notes retrieved","status":200,"data":json.loads(redis_note)},200
            note = Notes.query.filter_by(**kwargs).first()
            if note:
                return { "message": "Notes found","status":200,"data":note.json},200 
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
            RedisManager.delete(f'user_{kwargs['user_id']}',f'note_{kwargs['id']}')
            return {"message": "Note deleted successfully", "status" :204}, 204
        except Exception as e:
            return {'message': 'Something went wrong',"status": 500}, 500
