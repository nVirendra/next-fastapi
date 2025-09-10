from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List, Optional
from app.schemas.clt_user_schema import  UserRead,UserLogin, TokenResponse
from app.services.new_user_service import (get_users,login_user)
from app.auth import get_current_user


router = APIRouter(prefix="/new-users", tags=["NewUsers"])


@router.get("/", response_model=List[UserRead])
async def read_users(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = Query(None, description="Search by name or email"),
    current_user: dict = Depends(get_current_user)  # Inject authenticated user
):  
    print(f"Current user ID: {current_user['_id']}")  # You now have access to current user data
    return await get_users(current_user=current_user, skip=skip, limit=limit, search=search)

@router.post("/login", response_model=TokenResponse)
async def login(user_credentials: UserLogin):
    result = await login_user(user_credentials.email, user_credentials.password)
    if not result:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return result



