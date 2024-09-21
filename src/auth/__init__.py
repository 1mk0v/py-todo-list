from datetime import timedelta, datetime
import jwt
from .models import Token
import logging

logger = logging.getLogger('uvicorn.error')

class TokenCreater:

    def __init__(
            self,
            secret_key:str,
            algorithm:str,
            validity:int
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.validity = int(validity)

    def getJWT(self, sub:str, scopes:list = ['']) -> Token:
        access_token_expires = timedelta(minutes=self.validity)
        access_token = self.create_access_token(
            data={"sub": sub, "scopes": " ".join(scopes)},
            expires_delta=access_token_expires,
        )
        return Token(access_token=access_token, token_type='bearer')

    def create_access_token(self, data: dict, expires_delta: timedelta | None = timedelta(minutes=30)):
        logger.debug('Creating token...')
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt