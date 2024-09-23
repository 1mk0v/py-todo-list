from pydantic import BaseModel

class InsertingStatus(BaseModel):
    value:str
    description:str

class Status(InsertingStatus):
    id:int