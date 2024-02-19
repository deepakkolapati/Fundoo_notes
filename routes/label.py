from core import db, init_app
from flask import request, jsonify
from core.models import Label
from pydantic import ValidationError
from flask_restx import Api, Resource
from schemas.note_schemas import NoteValidator
import json
from core.middleware import authorize_user
from core.utils import RedisManager

app = init_app()
api = Api(app=app, prefix='/api')

@api.route("/labels", "/labels/<int:id>")
class LabelApi(Resource):
    method_decorators = (authorize_user,)
    def get(self,*args, **kwargs):
        try:
            user_id= kwargs["user_id"]
            labels=Label.query.filter_by(user_id=user_id).all()
            if not labels:
                return {"message":"Labels not found","status": 404 },404
            return {"message":"Labels found","status":200,
                    "data":[label.json for label in labels]},200
        except Exception as e :
            return {"message": str(e), "status": 500}, 500

    def post(self,*args, **kwargs):
        try:
            data = request.json
            label=Label(**data)
            db.session.add(label)
            db.session.commit()
            return {"message": "Label added successfully", "status": 201, "data": label.json}, 201
        except Exception as e:
            return {'message': str(e), "status": 500}, 500

    def put(self,*args, **kwargs):
        try:
            data=request.json
            label=Label.query.filter_by(id=data["id"], user_id=data["user_id"]).first()
            if not label:
                return {"message": "Label not found","status": 404 },404
            label.name=data["name"]
            db.session.commit()
            return {"message": "Label updated successfully", "status" :200,"data": label.json}, 200
        except Exception as e:
            return {"message": str(e), "status":500},500

    def delete(self,*args, **kwargs):
        try:
            label=Label.query.filter_by(id=kwargs["id"], user_id=kwargs["user_id"]).first()
            if not label:
                return {"message": "Label not found","status": 404 },404
            db.session.delete(label)
            db.session.commit()
            return {"message": "Label deleted successfully", "status" :204}, 204
        except Exception as e:
            return {"message": str(e), "status":500},500