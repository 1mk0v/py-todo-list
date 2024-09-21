from .settings import Settings
from sqlalchemy import Table, MetaData, Column, String, Integer, Boolean, DateTime, func, ForeignKey
import logging 

logger = logging.getLogger('uvicorn.error')
settings = Settings()
metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('login', String, nullable=False, unique=True),
    Column('password', String, nullable=False)
)

user_sessions = Table(
    'user_sessions',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('session', String, unique=True),
    Column('logined_datetime', DateTime, server_default=func.now()),
    Column('user_login', String),
    Column('is_active', Boolean, server_default='1')
)


metadata.create_all(settings.sync_engine)