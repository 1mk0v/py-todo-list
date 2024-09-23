from datetime import datetime
from pydantic import BaseModel

class Event(BaseModel):
    title:str
    description:str
    status_id: int
    deadline:datetime


