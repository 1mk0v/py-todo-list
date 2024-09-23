from fastapi import APIRouter, HTTPException, Depends
from auth.routers import getCurrentActiveUser
from exceptions import BaseAPIException, PermissionDenied
from typing import List, Any
from models import Event
from . import TaskTableInterface
from .models import Task, TaskEvent, InsertingTask
import logging

logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.post("/add")
async def add_task(data:TaskEvent, current_user:str=Depends(getCurrentActiveUser)) -> Task | Any:
    try:
        task = TaskTableInterface(user=current_user)
        insert_data = InsertingTask(
            title=data.title,
            description=data.description, 
            status_id=data.status_id,
            deadline=data.deadline,
            project_id=data.project_id,
            user=current_user
        )
        res = (await task.add(insert_data.model_dump())).fetchone()
        return res
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )

@router.put("/{id}/update")
async def update_task(id:int, data:Event, current_user:str=Depends(getCurrentActiveUser)) -> Task:
    try:
        project = TaskTableInterface(user=current_user)
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
async def update_status(id:int, new_status_id:int, current_user:str=Depends(getCurrentActiveUser)) -> Task:
    try:
        task = TaskTableInterface(user=current_user)
        res = (await task.update_status(id, new_status_id)).fetchone()
        if not res:
            raise PermissionDenied(message="Can't do this")
        return res
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )

@router.delete("/{id}/remove")
async def remove_project(id:int, current_user:str=Depends(getCurrentActiveUser)) -> Task:
    try:
        task = TaskTableInterface(user=current_user)
        res = (await task.delete(id, 'id')).fetchone()
        if not res:
            raise PermissionDenied(message="Can't do this")
        return res
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )