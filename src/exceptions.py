class BaseAPIException(BaseException):

    def __init__(self, *args: object, message:str = 'Base API exception!', status_code) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(*args)