from pydantic import BaseModel
from typing import Optional, List


class Module(BaseModel):
    id: Optional[str]
    name: str
    slug: str
    description: Optional[str] = None
    features: List[str] = []
    monthly_price: float
    yearly_price: float
    active: bool = True
