from pydantic import BaseModel
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

class User(BaseModel):
    login:str

class UserWithPWD(User):
    password:str | None

class UserWithHashedPWD(UserWithPWD):
    hashed_pwd:str

class UserDB(UserWithPWD):
    id:int

class UserSession(BaseException):
    id:int
    session:str
    logined_datetime:datetime
    user_id:int
    is_active:bool