from pydantic import BaseModel
from typing import Optional


class MenuCreate(BaseModel):
    name: str
    slug: str
    icon: Optional[str] = None
    path: str
    module: Optional[str] = None
    parent_id: Optional[str] = None
    active: bool = True


class MenuRead(MenuCreate):
    id: str
