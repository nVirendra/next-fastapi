from pydantic import BaseModel, EmailStr

class BusinessCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    active: bool = True

class BusinessRead(BusinessCreate):
    id: str