from typing import Optional
from pydantic import BaseModel

class Role(BaseModel):
    id: Optional[str]
    name: str
    description: Optional[str] = None
    active: bool = True