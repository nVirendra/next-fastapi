from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId

class User(BaseModel):
    id: Optional[str] = None
    first_name: str
    last_name: str
    name: Optional[str] = None
    role_id: str  
    email: EmailStr
    phone_no: str
