from auth.auth import UsersManager
import logging

logger = logging.getLogger('uvicorn.error')

async def create_user(login:str, password:str):
    u_manager = UsersManager()
    if await u_manager.is_user_exist(login):
        logger.info(f"User {login} is already exist")
        return
    return await u_manager.create_user(login=login, password=password)