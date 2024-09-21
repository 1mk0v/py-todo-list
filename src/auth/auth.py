from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from .models import UserWithPWD, UserWithHashedPWD
from . import TokenCreater
from . import exceptions as exc
from sqlalchemy import insert, select, update, and_, func
from datetime import datetime, time
from database.core import DBTableInterface
from database.users_store import (
    settings as users_store_settings, 
    schemas as users_schemas
)
from passlib.context import CryptContext
import logging 

logger = logging.getLogger('uvicorn.error')

class UsersManager:

    def __init__(self) -> None:
        self.users = DBTableInterface(
            table = users_schemas.users,
            engine = users_store_settings.Settings().async_engine
        )
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def is_user_exist(self, login:str) -> UserWithHashedPWD | bool:
        """Return user is exist, another return False"""
        user = (await self.users.get_by_column(value=login, column='login')).fetchone()
        logger.debug(f"Find user {user}")
        return UserWithHashedPWD(
            login=user._mapping['login'], 
            hashed_pwd=user._mapping['password'],
            password=None,
            id=user._mapping['id']
        ) if user else False

    async def check_user_or_raise_exception(self, login:str, password:str):
        try:
            user = await self.is_user_exist(login)
            if not user:
                logger.debug(f"Can't find user {login}")
                raise exc.NotFoundUserError()
            if not self._verify_password(password, user.hashed_pwd):
                logger.debug(f"Password for user {login} is incorrect!")
                raise exc.IncorrectPasswordError()
            return user
        except Exception as err:
            logger.error(err)
            raise exc.AuthException()

    async def create_user(self, login:str, password:str):
        try:
            hashed_password = self._get_password_hash(password)
            return await self.users.add({ "login": login , "password": hashed_password })
        except Exception as err:
            logger.error(err)
            raise exc.CreateUserError()

    def _verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def _get_password_hash(self, password):
        return self.pwd_context.hash(password)

class SessionManager:

    def __init__(self, validity_period:int) -> None:
        hours = int(validity_period/60)
        self.validity_period = {
            "hours": hours,
            "minutes": validity_period - hours*60
        }
        self.users_sessions = DBTableInterface(
            table = users_schemas.user_sessions,
            engine = users_store_settings.Settings().async_engine
        )

    async def create(self, token:str, user:int):
        stmt = insert(self.users_sessions.table).values({"session": token, "user_login": user})
        async with self.users_sessions.engine.connect() as conn:
            await conn.execute(stmt)
            await conn.commit()
        logger.debug(f'Created session for {user}')
        return True
    
    async def drop(self, token:str):
        query = update(self.users_sessions.table).where(
            self.users_sessions.table.c['session'] == token
            ).values(
                {'is_active': False}
            ).returning(self.users_sessions.table)
        async with self.users_sessions.engine.connect() as conn:
            res = await conn.execute(query)
            await conn.commit()
            id = res.fetchone().id
        logger.debug(f'Droped session id = {id}')
        return id

    async def get(self, user:str):
        logger.debug(f'Searching session of user {user}')
        access_token = time(hour=self.validity_period['hours'], minute=self.validity_period['minutes'], second=0,microsecond=0)
        query = select(self.users_sessions.table).where(
            and_(
                self.users_sessions.table.c['user_login'] == user,
                self.users_sessions.table.c['is_active'] == True,
                (func.current_timestamp() - self.users_sessions.table.c['logined_datetime']) < access_token
                )
            )
        async with self.users_sessions.engine.connect() as conn:
            res = (await conn.execute(query)).fetchone()
        logger.debug(f"Find session = {res}")
        return res


class Authenticator:

    def __init__(self) -> None:
        self.user_manager = UsersManager()
        self.token_creater = TokenCreater(SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)
        self.session = SessionManager(int(ACCESS_TOKEN_EXPIRE_MINUTES))

    async def authUser(self, user_data:UserWithPWD):
        await self.user_manager.check_user_or_raise_exception(login=user_data.login, password=user_data.password)
        return user_data.login