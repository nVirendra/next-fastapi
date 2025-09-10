from typing import Optional
from pydantic import BaseModel, EmailStr
from app.db.models.UserModel import User

# ----------------------
# User Schemas
# ----------------------

class UserCreate(User):
    pass

class UserRead(User):
    id: str

# ----------------------
# Login Request & Response
# ----------------------

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
