from models import Event

class InsertingProject(Event):
    user:str
class Project(Event):
    id: int
