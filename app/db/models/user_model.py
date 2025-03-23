from pydantic import BaseModel, EmailStr
from bson import ObjectId
from typing import Optional

class User(BaseModel):
    id: Optional[str] = None
    name: str
    email: EmailStr