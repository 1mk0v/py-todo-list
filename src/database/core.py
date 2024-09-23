from sqlalchemy import  Table, Engine, select, insert, update, delete, CursorResult
from sqlalchemy import exc as SQLException
from .exceptions import DBException, ConnectionTimeout,ConnectionBaseError, IntegrityError
import logging

logger = logging.getLogger('uvicorn.error')


class DBTableInterface():

    def __init__(self, table:Table, engine:Engine) -> None:
        self.table = table
        self.engine = engine

    async def execute_query(self, query) -> CursorResult:
        try:
            async with self.engine.connect() as conn:
                return await conn.execute(query)
        except TimeoutError:
            err = ConnectionTimeout(db_interface=self)
            logger.error(err.message)
            raise err
        except Exception as error:
            logger.error(error)
            raise ConnectionBaseError(db_interface=self)

    async def execute_stmt(self, stmt) -> CursorResult:
        try:
            async with self.engine.connect() as conn:
                result = await conn.execute(stmt)
                await conn.commit()
                return result
        except TimeoutError as error:
            logger.error(error)
            raise ConnectionTimeout(db_interface=self)
        except SQLException.IntegrityError as error:
            logger.error(error)
            detail = error.args[0].split('\n')[1].split(':  ')[1]
            raise IntegrityError(message=detail)
        except Exception as error:
            logger.error(error)
            raise DBException(db_interface=self)

    @property
    def base_query(self):
        return select(self.table)

    async def get(self, limit=10, offset=0):
        try:
            query = self.base_query.limit(limit).offset(offset)
            return await self.execute_query(query)
        except Exception as Error:
            logger.error(Error)
            raise DBException(db_interface=self)

    async def get_by_column(self, value, column:str = 'id'):
        try:
            query = self.base_query.where(self.table.c[column] == value)
            return await self.execute_query(query)
        except Exception as Error:
            logger.error(Error)
            raise DBException(db_interface=self)

    async def add(self, data:dict):
        try:
            stmt = insert(self.table).values(data).returning(self.table)
            return await self.execute_stmt(stmt)
        except DBException as err:
            raise err

    async def update(self, column, value, data:dict):
        try:
            stmt = (
                update(self.table)
                    .where(self.table.c[column] == value)
                    .values(self.convert_dict_to_sa_columns(data))
                    .returning(self.table)
                )
            return await self.execute_stmt(stmt)
        except SQLException as Error:
            logger.error(Error)
            raise DBException(db_interface=self)

    def convert_dict_to_sa_columns(self, data:dict):
        result = {}
        for key in data:
            new_key = self.table.c[key]
            result[new_key] = data[key]
        return result

    async def delete(self, value, column:str = 'id'):
        try:
            stmt = delete(self.table).where(self.table.c[column] == value).returning(self.table)
            return await self.execute_stmt(stmt)
        except SQLException as Error:
            logger.error(Error)
            raise DBException(db_interface=self)

    @property
    def model(self):
        return self.__model