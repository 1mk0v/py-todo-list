from .settings import Settings
from sqlalchemy import Table, MetaData, Column, String, Integer, DateTime, ForeignKey, Boolean
import logging 

logger = logging.getLogger('uvicorn.error')
settings = Settings()
metadata = MetaData()

statuses = Table(
    "statuses",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("value", String, unique=True),
    Column("description", String)
)

projects = Table(
    "projects",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String, unique=True),
    Column('description', String),
    Column('status_id', Integer, ForeignKey('statuses.id'), server_default="1"),
    Column('deadline', DateTime(timezone=True)),
    Column('user', String),
    Column('is_deleted', Boolean, default=False)
)

tasks = Table(
    "tasks",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('title', String),
    Column('description', String),
    Column('status_id', Integer, ForeignKey('statuses.id')),
    Column('deadline', DateTime(timezone=True)),
    Column('user', String),
    Column('is_deleted', Boolean, default=False)
)

# metadata.drop_all(settings.sync_engine)
metadata.create_all(settings.sync_engine)