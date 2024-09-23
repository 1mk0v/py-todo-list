from sqlalchemy import Engine, Table
from database.core import DBTableInterface
from database.projects_store import settings, schemas

class StatusTableInterface(DBTableInterface):
    
    def __init__(
            self, 
            table: Table = schemas.statuses, 
            engine: Engine = settings.Settings().async_engine
        ) -> None:
        super().__init__(table, engine)