from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.schemas.role_schema import RoleCreate, RoleRead
from app.services.role_service import (
    create_role,
    get_roles,
    get_role_by_id,
    update_role,
    delete_role
)

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RoleRead, status_code=201)
async def create_role_route(data: RoleCreate):
    return await create_role(data)

@router.get("/", response_model=List[RoleRead])
async def read_roles(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = Query(None, description="Search by role name")
):
    return await get_roles(skip=skip, limit=limit, search=search)

@router.get("/{role_id}", response_model=RoleRead)
async def read_role(role_id: str):
    role = await get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/{role_id}", response_model=RoleRead)
async def update_role_route(role_id: str, data: RoleCreate):
    updated = await update_role(role_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Role not found")
    return updated

@router.delete("/{role_id}")
async def delete_role_route(role_id: str):
    deleted = await delete_role(role_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Role not found")
    return {"message": "Role deleted successfully"}