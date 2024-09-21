from exceptions import BaseAPIException 
from fastapi import status

class AuthException(BaseAPIException):
    def __init__(self, *args: object, message: str = "Auth error!", status_code = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(*args, message = message, status_code = status_code)


class NotFoundUserError(AuthException):
    def __init__(self, *args: object, status_code = status.HTTP_404_NOT_FOUND,
                  message:str = "User don't found!") -> None:
        super().__init__(*args, message = message, status_code = status_code)


class IncorrectPasswordError(AuthException):
    def __init__(self, *args: object, status_code = status.HTTP_400_BAD_REQUEST,
                 message: str = "Incorrect password!",) -> None:
        super().__init__(*args, message = message, status_code = status_code)

class CreateUserError(AuthException):
    def __init__(self, *args: object, message: str = "Can't create user", status_code=status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(*args, message=message, status_code=status_code)