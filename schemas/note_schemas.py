from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class NoteValidator(BaseModel):
    title: Optional[str]= None
    description : Optional[str]= None
    color :Optional[str]= None
    reminder : Optional[str]= None
    user_id : int
    