from fastapi import APIRouter, HTTPException, Depends
from auth.routers import getCurrentActiveUser
from exceptions import BaseAPIException, PermissionDenied
from typing import List, Any
from tasks import TaskTableInterface
from tasks.models import Task
from . import ProjectTableInterface
from .models import Project, Event, InsertingProject
import logging

logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.get("/")
async def get_projects(limit:int = 10, offset:int = 0, current_user:str=Depends(getCurrentActiveUser)) -> List[Project] | Any:
    try:
        projects = ProjectTableInterface(user=current_user)
        res = await projects.get(limit, offset)
        return res.fetchall()
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )

@router.post("/add")
async def add_status(data:Event, current_user:str=Depends(getCurrentActiveUser)) -> Project | Any:
    try:
        project = ProjectTableInterface(user=current_user)
        insert_data = InsertingProject(
            title=data.title, 
            description=data.description, 
            status_id=data.status_id, 
            deadline=data.deadline, 
            user=current_user
        )
        res = await project.add(insert_data.model_dump())
        return res.fetchone()
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )
    
@router.get("/{id}/tasks")
async def get_projects_tasks(id:int, current_user:str=Depends(getCurrentActiveUser)) -> List[Task] | Any:
    try:
        task = TaskTableInterface(user=current_user)
        res = await task.get_by_column(id, 'project_id')
        return res.fetchall()
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )


@router.put("/{id}/update")
async def update_status(id:int, data:Event, current_user:str=Depends(getCurrentActiveUser)) -> Project | Any:
    try:
        project = ProjectTableInterface(user=current_user)
        res = (await project.update('id', id, data.model_dump())).fetchone()
        if not res:
            raise PermissionDenied(message="Can't do this")
        return res
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )


@router.put("/{id}/status/update")
async def update_status(id:int, new_status_id:int, current_user:str=Depends(getCurrentActiveUser)) -> Project | Any:
    try:
        project = ProjectTableInterface(user=current_user)
        res = (await project.update_status(id, new_status_id)).fetchone()
        if not res:
            raise PermissionDenied(message="Can't do this")
        return res
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )

@router.delete("/{id}/remove")
async def remove_project(id:int, current_user:str=Depends(getCurrentActiveUser)) -> Project | Any:
    try:
        project = ProjectTableInterface(user=current_user)
        res = (await project.delete(id, 'id')).fetchone()
        logger.debug(res)
        if not res:
            raise PermissionDenied(message="Can't do this")
        return res
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )