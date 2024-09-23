from sqlalchemy import URL, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from ..config import *
import logging

logger = logging.getLogger('uvicorn.error')

class Settings:
    def __init__(self, timeout_seconds=10) -> None:
        self.async_drivername='postgresql+asyncpg'
        self.sync_drivername='postgresql+psycopg'
        self.username=DB_USER
        self.password=DB_PASSWORD
        self.host=DB_HOST
        self.port=DB_PORT
        self.database=DB_PROJECTS_NAME
        self.timeout_seconds=timeout_seconds
        self.sync_url = URL.create(
            self.sync_drivername,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database,
        )
        self.async_url = URL.create(
            self.async_drivername,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.database
        )
    
    @property
    def sync_engine(self):
        return create_engine(self.sync_url)
    
    @property
    def async_engine(self):
        return create_async_engine(
            self.async_url, 
            connect_args={"timeout": self.timeout_seconds}
        )