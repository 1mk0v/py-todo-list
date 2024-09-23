from fastapi import HTTPException
from auth.auth import UsersManager
from statuses.routers import add_status
from statuses.models import InsertingStatus
import logging
import json

logger = logging.getLogger('uvicorn.error')

async def create_user(login:str, password:str):
    u_manager = UsersManager()
    if await u_manager.is_user_exist(login):
        logger.info(f"User {login} is already exist")
        return
    return await u_manager.create_user(login=login, password=password)

async def create_statuses(path_to_file):
    with open(path_to_file, 'r') as statuses:
        statuses_json = statuses.read()
        status_list = json.loads(statuses_json)
        for status in status_list:
            try:
                res = await add_status(InsertingStatus(
                    value=status['value'],
                    description=status['description']
                    )
                )
                logger.debug(f"Status added {res.id}")
            except HTTPException as err:
                logger.debug(err.detail)
        logger.debug("Statuses added!")
