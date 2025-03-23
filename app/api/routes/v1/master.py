from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.schemas.master_schema import MasterCreate, MasterRead
from app.services.master_service import (
    create_master,
    get_masters,
    get_master_by_id,
    update_master,
    delete_master,
)

router = APIRouter(prefix="/masters", tags=["Masters"])


@router.post("/", response_model=MasterRead, status_code=201)
async def create(master: MasterCreate):
    return await create_master(master)


@router.get("/", response_model=List[MasterRead])
async def read_masters(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = Query(None, description="Search by label or value"),
    type: Optional[str] = Query(None, description="Filter by master type"),
):
    return await get_masters(skip=skip, limit=limit, search=search, type=type)


@router.get("/{master_id}", response_model=MasterRead)
async def read_master(master_id: str):
    master = await get_master_by_id(master_id)
    if not master:
        raise HTTPException(status_code=404, detail="Master not found")
    return master


@router.put("/{master_id}", response_model=MasterRead)
async def update(master_id: str, master: MasterCreate):
    updated = await update_master(master_id, master)
    if not updated:
        raise HTTPException(status_code=404, detail="Master not found")
    return updated


@router.delete("/{master_id}")
async def delete(master_id: str):
    deleted = await delete_master(master_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Master not found")
    return {"message": "Master deleted successfully"}
