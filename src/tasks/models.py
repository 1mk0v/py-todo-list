from models import Event

class TaskEvent(Event):
    project_id:int

class InsertingTask(TaskEvent):
    user:str

class Task(InsertingTask):
    id:int