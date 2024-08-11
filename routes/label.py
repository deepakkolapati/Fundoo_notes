from core import db, init_app
from flask import request, jsonify
from core.models import Label,Notes
from pydantic import ValidationError
from flask_restx import Api, Resource,fields
from schemas.note_schemas import NoteValidator
import json
from core.middleware import authorize_user
from core.utils import RedisManager
from sqlalchemy import text
import psycopg2
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy.exc import IntegrityError


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
        doc="/docs",default_label="Label", title="Fundoo Label", default="Fundoo")
limiter = Limiter(app=app,key_func=get_remote_address, storage_uri="redis://localhost:6379/1")

@api.route("/labels/<int:id>")
class LabelDeleteApi(Resource):
    method_decorators = (authorize_user,)
    @limiter.limit('20 per second')
    def delete(self,*args, **kwargs):
        """Deletes a label with the given id and user_id.

        Args:
            id (int): The id of the label to be deleted.
            user_id (int): The id of the user who owns the label.

        Returns:
            Response: A response with a status code of 204 if the label was
                deleted successfully, or a status code of 500 if an error occurred.
        """
        try:
            statement=text(f'''DELETE FROM labels WHERE id={kwargs["id"]} AND user_id={kwargs["user_id"]} ''')
            db.session.execute(statement)
            db.session.commit()
            return {"message": "Label deleted successfully", "status" :204}, 204
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status":500},500

@api.route("/labels")
class LabelApi(Resource):
    method_decorators = (authorize_user,)
    @api.expect(api.model('AddLabel', {"name": fields.String()}))
    @limiter.limit('20 per second')
    def post(self,*args, **kwargs):
        """
        Adds a new label to the database.

        Args:
            request (Request): The request containing the label data.

        Returns:
            Response: A response containing the label data and a status code of 201
                if the label was added successfully, or a status code of 500 if an
                error occurred.
        """
        try:
            data = request.json
            statement=text(f'''INSERT INTO labels(name,user_id) VALUES('{data["name"]}',{data["user_id"]})''')
            db.session.execute(statement)
            db.session.commit()
            query = db.session.execute(text("select * from labels order by id desc limit 1"))
            label = query.fetchone()
            columns = ([col[0] for col in query.cursor.description])
            data = dict(zip(columns, label))
            return {"message": "Label added successfully", "status": 201, "data": data}, 201
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {'message': str(e), "status": 500}, 500
    
    @api.expect(api.model('UpdateLabel', {"id":fields.Integer(),"name": fields.String()}))
    @limiter.limit('20 per second')
    def put(self,*args, **kwargs):
        """
        Update a label with the given id and user_id.

        Args:
            id (int): The id of the label to be updated.
            user_id (int): The id of the user who owns the label.
            name (str): The new name of the label.

        Returns:
            Response: A response with a status code of 200 if the label was updated
                successfully, or a status code of 500 if an error occurred.
        """
        try:
            data=request.json
            statement=text(f'''UPDATE labels SET name='{data["name"]}' WHERE id={data["id"]} AND user_id={data["user_id"]}''')
            db.session.execute(statement)
            db.session.commit()
            query = db.session.execute(text(f"select * from labels where id={data["id"]} AND user_id={data["user_id"]}"))
            label = query.fetchone()
            columns = ([col[0] for col in query.cursor.description])
            data = dict(zip(columns, label))
            return {"message": "Label updated successfully", "status" :200,"data": data}, 200
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status":500},500
            
    @limiter.limit('20 per second')
    def get(self,*args, **kwargs):
        """
        Retrieve all labels for a given user.

        Parameters:
            user_id (int): The user ID associated with the labels.

        Returns:
            list[dict]: A list of label dictionaries, each containing the label
                properties.

        Raises:
            Exception: An exception is raised if an error occurs.
        """

        try:
            labels=Label.query.filter_by(user_id=kwargs["user_id"]).all()
            if labels:
                label_notes=[]
                for label in labels:
                    notes=[note.json for note in label.c_notes]
                    label_notes.append({"label_name":label.name,"notes":notes})
                return {"message":"Labels found","labels": label_notes,"status": 200},200

            return {"message" : "Labels are not found", "status": 404},404
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status": 500}, 500

@api.route("/association")
class AssociationApi(Resource):
    method_decorators=(authorize_user,)

    @api.expect(api.model("AddNotesLabel",{"id":fields.Integer(),"note_ids": fields.List(fields.Integer)}))
    def post(self,*args,**kwargs):
        try:
            data=request.json
            label=Label.query.filter_by(id=data["id"],user_id=data["user_id"]).first()
            if not label:
                return {"message":"Label not found","status":404},404

            notes_to_associate=[Notes.query.filter_by(id=id,user_id=data["user_id"]).first() #
            for id in data["note_ids"]]
            
            if notes_to_associate:
                label.c_notes.extend(notes_to_associate)
                db.session.commit()
                note_ids=[note.id for note in notes_to_associate]
                return {"message":f"Label_{label.id} is associated successfully with notes {','.join(map(str,note_ids))}",
                "status" : 201},201
            return {"message":"Label can't be associated with the given notes"}

        except IntegrityError as e:
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status": 409}, 409
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status": 500}, 500
    
    @api.expect(api.model("DeleteNotesLabel",{"id":fields.Integer(),"note_ids": fields.List(fields.Integer)}))
    def delete(self,*args,**kwargs):
        try:
            data=request.json
            label=Label.query.filter_by(id=data["id"],user_id=kwargs["user_id"]).first()
            if not label:
                return {"message":"Label not found","status":404},404
            
            notes_to_disassociate=[Notes.query.filter_by(id=id,user_id=kwargs["user_id"]).first() #
            for id in data["note_ids"]]

            if notes_to_disassociate:
                [label.c_notes.remove(note) for note in notes_to_disassociate]
                note_ids=[note.id for note in notes_to_disassociate]
                db.session.commit()
                return {"message":f"Label_{label.id} is disassociated successfully with notes {','.join(map(str,note_ids))} ",
                 "status":204},204
            
            return {"message":"Label can't be disassociated with the given notes"}
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status": 500}, 500




            


            



