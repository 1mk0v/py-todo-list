from sqlalchemy import Engine, Table, update
from database.core import DBTableInterface
from database.projects_store import settings, schemas

class ProjectTableInterface(DBTableInterface):
    
    def __init__(
            self, 
            table: Table = schemas.projects, 
            engine: Engine = settings.Settings().async_engine
        ) -> None:
        super().__init__(table, engine)

    async def update_status(self, project_id:int, new_status_id:int):
        stmt = (
            update(self.table)
                .where(self.table.c['id'] == project_id)
                .values(status_id = new_status_id)
                .returning(self.table)
        )
        return await self.execute_stmt(stmt)
        