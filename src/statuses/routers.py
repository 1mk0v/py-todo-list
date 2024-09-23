from fastapi import APIRouter, HTTPException, Depends
from auth.routers import getCurrentActiveUser
from exceptions import BaseAPIException
from typing import List
from . import StatusTableInterface
from .models import Status, InsertingStatus
import logging

logger = logging.getLogger('uvicorn.error')

router = APIRouter(
    prefix="/statuses",
    tags=["Statuses"],
    dependencies=[Depends(getCurrentActiveUser)]
)

@router.get("/")
async def get_statuses(limit:int = 10, offset:int = 0) -> List[Status]:
    try:
        status = StatusTableInterface()
        res = await status.get(limit, offset)
        return res.fetchall()
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )

@router.post("/add")
async def add_status(data:InsertingStatus) -> Status:
    try:
        status = StatusTableInterface()
        res = await status.add(data.model_dump())
        return res.fetchone()
    except BaseAPIException as err:
        raise HTTPException(
            status_code=err.status_code,
            detail=err.message
        )