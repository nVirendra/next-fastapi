from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.schemas.user import UserCreate, UserRead
from app.services.user_service import (
    create_user,
    get_users,
    get_user_by_id,
    update_user,
    delete_user
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserRead, status_code=201)
async def create(user: UserCreate):
    return await create_user(user)


@router.get("/", response_model=List[UserRead])
async def read_users(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = Query(None, description="Search by name or email")
):
    return await get_users(skip=skip, limit=limit, search=search)


@router.get("/{user_id}", response_model=UserRead)
async def read_user(user_id: str):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update(user_id: str, user: UserCreate):
    updated_user = await update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}")
async def delete(user_id: str):
    deleted = await delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
