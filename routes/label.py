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

@api.route("/labels/<int:id>")
class LabelApi(Resource):
    method_decorators = (authorize_user,)
    def delete(self,*args, **kwargs):
        try:
            statement=text(f'''SELECT * FROM labels WHERE id={kwargs["id"]} AND user_id={kwargs["user_id"]}''')
            label=db.session.execute(statement).fetchone()
            if not label:
                return {"message": "Label not found","status": 404 },404
            statement=text(f'''DELETE FROM labels WHERE id={kwargs["id"]} AND user_id={kwargs["user_id"]} ''')
            db.session.execute(statement)
            db.session.commit()
            return {"message": "Label deleted successfully", "status" :204}, 204
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status":500},500

@api.route("/labels")
class LabelPostApi(Resource):
    method_decorators = (authorize_user,)
    @api.expect(api.model('AddLabel', {"name": fields.String()}))
    def post(self,*args, **kwargs):
        try:
            data = request.json
            statement=text(f'''INSERT INTO labels(name,user_id) VALUES('{data["name"]}',{data["user_id"]})''')
            db.session.execute(statement)
            db.session.commit()
            return {"message": "Label added successfully", "status": 201, "data": data}, 201
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {'message': str(e), "status": 500}, 500
    
    @api.expect(api.model('UpdateLabel', {"id":fields.Integer(),"name": fields.String()}))
    def put(self,*args, **kwargs):
        try:
            data=request.json
            statement=text(f'''SELECT * FROM labels WHERE id={data["id"]} AND user_id={data["user_id"]}''')
            label=db.session.execute(statement).fetchone()
            if not label:
                return {"message": "Label not found","status": 404 },404
            statement=text(f'''UPDATE labels SET name='{data["name"]}' WHERE id={data["id"]} AND user_id={data["user_id"]}''')
            db.session.execute(statement)
            db.session.commit()
            return {"message": "Label updated successfully", "status" :200,"data": data}, 200
        except Exception as e:
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status":500},500
    
    def get(self,*args, **kwargs):
        try:
            user_id= kwargs["user_id"]
            statement = text(f"SELECT * FROM labels WHERE user_id = {user_id}")
            result = db.session.execute(statement).fetchall()
            labels=[{'id':row[0],'name':row[1],'user_id':row[2]} for row in result]
            if not labels:
                return {"message":"Labels not found","status": 404 },404
            return {"message":"Labels found","status":200,
                    "data":labels},200
        except Exception as e :
            app.logger.exception(e,exc_info=False)
            return {"message": str(e), "status": 500}, 500
