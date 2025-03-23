from typing import Optional
from pydantic import BaseModel, EmailStr

class Business(BaseModel):
    id: Optional[str]
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    active: bool = True