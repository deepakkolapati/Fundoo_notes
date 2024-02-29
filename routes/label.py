from core import db, init_app
from flask import request, jsonify
from core.models import Label
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
            user_id= kwargs["user_id"]
            query= db.session.execute(text(f"SELECT * FROM labels WHERE user_id = {user_id}"))
            labels=list(map(dict, query.mappings().all()))
            if labels:
                return {"message":"Labels found","status":200,
                    "data": labels},200
            return {"message":"Labels not found","status":404},404
        except Exception as e :
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status": 500}, 500
