from fastapi import FastAPI
import config
import logging
import utils
from auth import routers as auth_routers

logger = logging.getLogger('uvicorn.error')

app:FastAPI = FastAPI(
    title="TaskManager API",
    description="",
    version="0.1.0"
)

app.include_router(auth_routers.router)

@app.on_event('startup')
async def wake_up_app():
    logger.info("Creating ROOT user...")
    await utils.create_user(config.ROOT_LOGIN, config.ROOT_PASSWORD)