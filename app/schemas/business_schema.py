from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime

# Custom field for ObjectId reference
class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

class Address(BaseModel):
    street: str
    city: str
    state: str
    postal_code: str
    country: PyObjectId

class BusinessCreate(BaseModel):
    business_name: str
    business_slug: str
    registration_number: str
    contact_number: str
    email: EmailStr
    address: Address
    business_type: PyObjectId
    business_category: PyObjectId
    status: str = "active"

class BusinessRead(BusinessCreate):
    id: str
    createdAt: datetime
    updatedAt: datetime
