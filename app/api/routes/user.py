from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import (
    create_user, get_users, get_user_by_id,
    update_user, delete_user
)

router = APIRouter()

@router.post("/users", response_model=UserRead)
def create(user: UserCreate):
    return create_user(user)

@router.get("/users", response_model=List[UserRead])
def read_users(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = Query(None, description="Search by name or email")
):
    return get_users(skip=skip, limit=limit, search=search)

@router.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: str):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserRead)
def update(user_id: str, user: UserCreate):
    updated_user = update_user(user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}")
def delete(user_id: str):
    deleted = delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
