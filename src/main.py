from fastapi import FastAPI
import config
import logging
import utils
from auth import routers as auth_routers
from projects import routers as projects_routers
from tasks import routers as tasks_routers
from statuses import routers as status_routers

logger = logging.getLogger('uvicorn.error')

app:FastAPI = FastAPI(
    title="TaskManager API",
    description="",
    version="0.1.0"
)

app.include_router(auth_routers.router)
app.include_router(projects_routers.router)
app.include_router(tasks_routers.router)
app.include_router(status_routers.router)


@app.on_event('startup')
async def wake_up_app():
    logger.info("Creating ROOT user...")
    await utils.create_user(config.ROOT_LOGIN, config.ROOT_PASSWORD)
    logger.info("Creating default statuses...")
    await utils.create_statuses(config.PATH_TO_DEFAULT_STATUSES)