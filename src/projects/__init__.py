from sqlalchemy import Engine, Table, update, select
from database.core import DBTableInterface, SQLException, DBException
from database.projects_store import settings, schemas
import logging

logger = logging.getLogger('uvicorn.error')

class ProjectTableInterface(DBTableInterface):
    
    def __init__(
            self, 
            table: Table = schemas.projects, 
            engine: Engine = settings.Settings().async_engine,
            user: str = None
        ) -> None:
        super().__init__(table, engine, user)

    @property
    def base_query(self):
        return select(self.table).where(
            self.table.c['is_deleted'] == False,
            self.table.c['user'] == self.user
        )


    async def update_status(self, project_id:int, new_status_id:int):
        stmt = (
            update(self.table)
                .where(
                    self.table.c['id'] == project_id,
                    self.table.c['is_deleted'] == False,
                    self.table.c['user'] == self.user
                )
                .values(status_id = new_status_id)
                .returning(self.table)
        )
        return await self.execute_stmt(stmt)
    
    async def update(self, column, value, data: dict):
        stmt = (
            update(self.table)
                .where(
                    self.table.c[column] == value,
                    self.table.c['is_deleted'] == False,
                    self.table.c['user'] == self.user
                )
                .values(self.convert_dict_to_sa_columns(data))
                .returning(self.table)
            )
        return await self.execute_stmt(stmt)
    

    async def delete(self, value, column:str = 'id'):
        try:
            stmt = (
                update(self.table)
                    .where(
                        self.table.c[column] == value,
                        self.table.c['is_deleted'] == False,
                        self.table.c['user'] == self.user
                    )
                    .values(is_deleted = True)
                    .returning(self.table)
            )
            return await self.execute_stmt(stmt)
        except SQLException as Error:
            logger.error(Error)
            raise DBException(db_interface=self)