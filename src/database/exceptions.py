from exceptions import BaseAPIException

class DBException(BaseAPIException):
    def __init__(self, *args: object, db_interface = None, message: str = '', status_code = 400) -> None:
        if message == '':
            message = f'An error occurred while working with the database {db_interface.engine.url.database} on {db_interface.engine.url.host}:{db_interface.engine.url.port}'
        super().__init__(*args, message=message, status_code=status_code)

class ConnectionBaseError(DBException):
    def __init__(self, *args: object, db_interface = None, message: str = '', status_code = 400) -> None:
        if message == '':
            message = f'Something happened when connecting to the database {db_interface.engine.url.database} on {db_interface.engine.url.host}:{db_interface.engine.url.port}'
        super().__init__(*args, message=message, status_code=status_code)

class ConnectionTimeout(DBException):
    def __init__(self, *args: object, db_interface = None,  message: str = '', status_code=400) -> None:
        if message == '':
            message = f'Exceeded the waiting limit when connecting to the database {db_interface.engine.url.database} on {db_interface.engine.url.host}:{db_interface.engine.url.port}'
        super().__init__(*args, message=message, status_code=status_code)

class IntegrityError(DBException):
    def __init__(self, *args: object, db_interface=None, message: str = '', status_code=400) -> None:
        if message == '':
            message = f'Detection of violation of restrictions on database {db_interface.engine.url.database} on {db_interface.engine.url.host}:{db_interface.engine.url.port}'
        super().__init__(*args, db_interface=db_interface, message=message, status_code=status_code)