from fastapi import APIRouter, HTTPException, Depends
from auth.routers import getCurrentActiveUser
from exceptions import BaseAPIException
from typing import List
from . import ProjectTableInterface
from .models import Project, Event
import logging

logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    dependencies=[Depends(getCurrentActiveUser)]
)

@router.get("/")
async def get_projects(limit:int = 10, offset:int = 0) -> List[Project]:
    try:
        projects = ProjectTableInterface()
        res = await projects.get(limit, offset)
        return res.fetchall()
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )

@router.post("/add")
async def add_status(data:Event) -> Project:
    try:
        project = ProjectTableInterface()
        res = await project.add(data.model_dump())
        return res.fetchone()
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )
    
# @router.put("/{project_id}/tasks")
# async def get_projects_tasks(project_id:int) -> Project:
#     try:
#         project = ProjectTableInterface()
#         res = await project.get_by_column()
#         return res.fetchone()
#     except BaseAPIException as err:
#         raise HTTPException(
#             status_code=err.status_code,
#             detail=err.message
#         )

@router.put("/{project_id}/update")
async def update_status(project_id:int, data:Event) -> Project:
    try:
        project = ProjectTableInterface()
        res = await project.update('id', project_id, data.model_dump())
        return res.fetchone()
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )

@router.put("/{project_id}/status/update")
async def update_status(project_id:int, new_status_id:int) -> Project:
    try:
        project = ProjectTableInterface()
        res = await project.update_status(project_id, new_status_id)
        return res.fetchone()
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )