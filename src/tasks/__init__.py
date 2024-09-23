from sqlalchemy import Engine, Table
from database.core import SQLException, DBException
from database.projects_store import settings, schemas
from projects import ProjectTableInterface
import logging

logger = logging.getLogger('uvicorn.error')

class TaskTableInterface(ProjectTableInterface):
    
    def __init__(
            self, 
            table: Table = schemas.tasks, 
            engine: Engine = settings.Settings().async_engine,
            user: str = None
        ) -> None:
        super().__init__(table, engine, user)

    async def update_status(self, task_id: int, new_status_id: int):
        return await super().update_status(task_id, new_status_id)