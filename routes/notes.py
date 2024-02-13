from core import db, init_app
from flask import request,jsonify
from core.models import Notes
from pydantic import ValidationError
import json
from flask_restx import Api, Resource
from schemas.note_schemas import NoteValidator

app = init_app()
api = Api(app=app, prefix='/api')

@api.route("/notes")
class NotesApi(Resource):
    def post(self):
        try:
            serializer=NoteValidator(**request.get_json())
            note=Notes(**serializer.model_dump())
            db.session.add(note)
            db.session.commit()
            return {"message": "Notes added Successfully"},201
        except ValidationError as e:
            pass

    def get(self):
        try:
            data=request.json
        except Exception as e:
            pass




