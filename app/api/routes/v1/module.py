from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.module_schema import ModuleCreate, ModuleRead
from app.services.module_service import (
    create_module,
    get_modules,
    get_module_by_id,
    update_module,
    delete_module
)

router = APIRouter(prefix="/modules", tags=["Modules"])


@router.post("/", response_model=ModuleRead, status_code=201)
async def create(data: ModuleCreate):
    return await create_module(data)


@router.get("/", response_model=List[ModuleRead])
async def read_all(skip: int = 0, limit: int = 20, search: Optional[str] = Query(None)):
    return await get_modules(skip=skip, limit=limit, search=search)


@router.get("/{module_id}", response_model=ModuleRead)
async def read_one(module_id: str):
    module = await get_module_by_id(module_id)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


@router.put("/{module_id}", response_model=ModuleRead)
async def update(module_id: str, data: ModuleCreate):
    updated = await update_module(module_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Module not found")
    return updated


@router.delete("/{module_id}")
async def delete(module_id: str):
    deleted = await delete_module(module_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Module not found")
    return {"message": "Module deleted successfully"}
