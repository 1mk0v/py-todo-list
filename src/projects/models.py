from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel):
    title:str
    description:str
    status_id: int
    deadline:datetime

class Project(Event):
    id: int

class InsertingTask(Event):
    project_id:int

class Task(InsertingTask):
    id:int