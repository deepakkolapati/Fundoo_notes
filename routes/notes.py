from core import db, init_app
from flask import request, jsonify
from core.models import Notes
from core.models import User
from core.models import collaborators
from pydantic import ValidationError
from flask_restx import Api, Resource,fields
from schemas.note_schemas import NoteValidator
import json
from core.middleware import authorize_user
from core.utils import RedisManager
from sqlalchemy.exc import IntegrityError
from redbeat import RedBeatSchedulerEntry as Task
from celery.schedules import crontab
from core.tasks import celery as c_app
import celery

app = init_app()
api = Api(app=app, prefix='/api',
        security='apiKey',
        authorizations={
            'apiKey': {
                'type': 'apiKey',
                'in': 'header',
                'required': True,
                'name': 'Authorization'
            }
        },
        doc="/docs")

@api.route("/notes")
class NotesApi(Resource):

    method_decorators =(authorize_user,)
    @api.expect(api.model('AddNotes', {"title": fields.String(),
    "description": fields.String() ,
    "color": fields.String(),
     "reminder": fields.DateTime(attribute=lambda x: None if x == 'None' else datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ'))}))
    def post(self, *args, **kwargs):
        try:
            serializer = NoteValidator(**request.get_json())
            note = Notes(**serializer.model_dump())
            db.session.add(note)
            db.session.commit()
            reminder = note.reminder
            if reminder:
                reminder_task = Task(name=f'user_{note.user_id}-note_{note.id}',
                task='core.tasks.celery_send_mail',
                schedule=crontab(minute=reminder.minute,
                hour=reminder.hour,
                day_of_month=reminder.day,
                month_of_year=reminder.month),
                app = c_app,
                args= [note.user.username, note.user.email, "Hello world"])
                reminder_task.save()
            # RedisManager.save(f'user_{note.user_id}',f'note_{note.id}', json.dumps(note.json))
            return {"message": "Note added successfully", 'status': 201, 'data': note.json}, 201
        except ValidationError as e:
            app.logger.exception(e,exc_info=False)
            err = json.loads(e.json())
            return {'message': f'{err[0]["input"]}-{err[0]["msg"]}', "status": 400}, 400
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {'message': str(e),'status': 500}, 500
    
    def get(self, *args, **kwargs):
        try:
            user_id = kwargs.get('user_id')
            if not user_id:
                return {'message': 'User ID not provided','status': 400}, 400
            
            user=User.query.filter_by(id=user_id).first()
            if not user:
                return {'message': 'User not found in database','status':   404}, 404
            
            shared_notes=[note.json for note in user.c_notes]
            # redis_note=RedisManager.get(f'user_{user_id}')
            
            # if redis_note:
            #     reddis_notes=[json.loads(value) for value in redis_note.values()]
            #     return {"message":"Notes Found","status":200,
            #             "data": reddis_notes,"shared data":shared_notes},200
            notes = Notes.query.filter_by(user_id=user_id).all()
            if notes:
                db_notes=[json.loads(value) for value in notes.values()]
                return {"message": " Notes Found","status":200,
                        "data": db_notes,"message":"Shared Notes","shared data":shared_notes},200
        
            return {"message": "Notes not found",'status': 404},404
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {'message': str(e),'status':500}, 500
    
    @api.expect(api.model('UpdateNotes', {"id":fields.Integer(),"title": fields.String(),
    "description": fields.String() ,
    "color": fields.String(),
     "reminder": fields.DateTime(attribute=lambda x: None if x == 'None' else datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%fZ'))}))
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
            # RedisManager.save(f'user_{note.user_id}',f'note_{note.id}', json.dumps(note.json))
            return {"message": "Note updated successfully","status":200,"data":note.json}, 200
        except ValidationError as e:
            app.logger.exception(e,exc_info=False)
            err = json.loads(e.json())
            return {'message': f'{err[0]["input"]}-{err[0]["msg"]}', "status": 400}, 400
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {'message': str(e),"status": 500}, 500


@api.route("/notes/<int:id>")
class NoteApi(Resource):

    method_decorators = (authorize_user,)

    def get(self, *args, **kwargs):
        try:
            # redis_note=RedisManager.get_one(f'user_{kwargs['user_id']}',f'note_{kwargs['id']}')
            # if redis_note:
            #     return { "message": "Notes found","status":200,"data":json.loads(redis_note)},200
            note = Notes.query.filter_by(**kwargs).first()
            if note:
                return { "message": "Notes found","status":200,"data":note.json},200
            user=User.query.filter_by(id=kwargs['user_id']).first() 
            if user:
                for note in user.c_notes:
                    if note.id==kwargs['id']:
                        return { "message": "Shared Notes found","status":200,"data":note.json},200
            return {"message": "Note not found", "status" : 404 }, 404
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {'message': str(e), "status": 500}, 500

    def delete(self, *args, **kwargs):
        try:
            note = Notes.query.filter_by(**kwargs).first()
            if not note:
                return {"message": "Note not found", "status" :404}, 404

            db.session.delete(note)
            db.session.commit()
            # RedisManager.delete(f'user_{kwargs['user_id']}',f'note_{kwargs['id']}')
            return {"message": "Note deleted successfully", "status" :204}, 204
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {'message': str(e),"status": 500}, 500


@api.route("/archive")
class ArchiveApi(Resource):

    method_decorators = (authorize_user,)
    @api.expect(api.model('PutArchive', {"id":fields.Integer()}))
    def patch(self,*args, **kwargs):
        try:
            data = request.json
            note=Notes.query.filter_by(id=data['id'],user_id=data['user_id']).first()
            if not note:
                return {"message":"Note not found","status": 404 },404
            note.is_archive = True if not note.is_archive else False
            db.session.commit()
            if not note.is_archive:
                return {"message":"Note is unarchived","status":200,"data" :note.json},200
            return {"message" : "Note is archived","status": 200,"data" : note.json},200
        except ValueError as e:
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status" :500},500

    def get(self,*args,**kwargs):
        try:
            user_id=kwargs["user_id"]
            notes=Notes.query.filter_by(user_id=user_id,is_archive=True, is_trash=False).all()
            if not notes:
                return {"message":"Notes not found","status": 404 },404
            return {"message":"Retrieved archive notes","status":200,
                    "data":[note.json for note in notes]},200
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status" :500},500

@api.route("/trash")
class TrashApi(Resource):
   
    method_decorators = (authorize_user,)
    @api.expect(api.model('PutTrash', {"id":fields.Integer()}))
    def patch(self,*args, **kwargs):
        try:
            data = request.json
            note=Notes.query.filter_by(id=data['id'],user_id=data['user_id']).first()
            if not note:
                return {"message":"Note not found","status": 404 },404
            note.is_trash = True if not note.is_trash else False
            db.session.commit()
            if not note.is_trash:
                return {"message":"Note is restored","status":200},200
            return {"message" : "Note moved to Trash","status": 200},200
        except ValueError as e:
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status" :500},500

    def get(self,*args,**kwargs):
        try:
            user_id=kwargs["user_id"]
            notes=Notes.query.filter_by(user_id=user_id,is_trash=True, is_archive=False).all()
            if not notes:
                return {"message":"Notes not found","status": 404 },404
            return {"message":"Retrieved trash notes","status":200,
                    "data":[note.json for note in notes]},200
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status" :500},500



@api.route("/collaborate")
class CollaborateApi(Resource):
    method_decorators = (authorize_user,)
    @api.expect(api.model('AddColaborators', {"id":fields.Integer(),"user_ids":fields.List(fields.Integer)}))
    def post(*args, **kwargs):
        try:
            data=request.json
            if data['user_id'] in data["user_ids"]:
                return {"message":"Sharing not allowed on the same user","status":403},403
            note=Notes.query.filter_by(id=data["id"],user_id=data["user_id"]).first()
            if not note:
                return {"message":"Note not found","status":404},404
            try:
                users_to_add = [User.query.filter_by(id=id).first() for id in data["user_ids"]]
                existing_collaborators=set(note.c_users)
                users_to_add=[user for user in users_to_add if user not in existing_collaborators]
                note.c_users.extend(users_to_add)
                db.session.commit()
                added_users=[user.id for user in users_to_add]
                if added_users:
                    return {"message":f"Note_{note.id} shared with users {",".join(map(str,added_users))}", "status": 201},201
                return {"message" : "Note can't be shared with the users who already have access","status":403},403
            except sqlalchemy.exc.IntegrityError as e:
                app.logger.exception(e,exc_info=False)
                return {"message":str(e),"status":409},409
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message":str(e),"status" :500},500
            
    @api.expect(api.model('RemoveColaborators', {"id":fields.Integer(),"user_ids":fields.List(fields.Integer)}))
    def delete(self,*args,**kwargs):
        try:
            data=request.json
            if kwargs['user_id'] in data["user_ids"]:
                return {"message":"Collaboration not allowed on the same user","status":403},403
            note=Notes.query.filter_by(id=data["id"],user_id=kwargs["user_id"]).first()
            
            if not note:
                return {"message":"Note not found","status":404},404
            try:
                users_to_delete=[User.query.filter_by(id=id).first() for id in data["user_ids"]]
                existing_collaborators=set(note.c_users)
                users_to_delete=[user for user in users_to_delete if user in existing_collaborators]
                [note.c_users.remove(user) for user in users_to_delete]
                db.session.commit()
                deleted_users=[user.id for user in users_to_delete]
                if deleted_users:
                    return {"message":f"Note_{note.id} access removed from users {",".join(map(str,deleted_users))}", "status": 201},201
                return {"message" : "Note can't be removed from the users who don't have access","status":403},403
            except sqlalchemy.exc.IntegrityError as e:
                app.logger.exception(e,exc_info=False)
                return {"message":str(e),"status":409},409
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message":str(e),"status" :500},500

        

