from typing import Optional, List, Literal
from pydantic import BaseModel, Field, EmailStr, constr
from datetime import datetime, timezone
from uuid import uuid4

Gender = Literal["male", "female", "non-binary"]

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

class User(BaseModel):
    id: Optional[str] = None
    user_id: str = Field(default_factory=lambda: uuid4().hex)
    username: str
    name: str = Field(..., min_length=1, max_length=80)
    email: EmailStr
    country: str = Field(..., min_length=2, max_length=56)
    join_date: datetime = Field(default_factory=now_utc)
    gender: Gender
    age: int = Field(..., ge=13, le=120)
    # hobbies: List[str] = Field(default_factory=list)
    hobbies: str
    education: Optional[str] = None


