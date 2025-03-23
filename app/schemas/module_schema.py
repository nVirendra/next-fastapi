from pydantic import BaseModel
from typing import Optional, List


class ModuleCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    features: List[str] = []
    monthly_price: float
    yearly_price: float
    active: bool = True


class ModuleRead(ModuleCreate):
    id: str
