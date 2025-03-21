from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserRead
from app.services.user_service import create_user, get_users

router = APIRouter()

@router.post("/users", response_model=UserRead)
def create(user: UserCreate):
    return create_user(user)

@router.get("/users", response_model=list[UserRead])
def read_users():
    return get_users()