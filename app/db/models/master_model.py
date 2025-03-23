from pydantic import BaseModel
from typing import Optional, Literal
from bson import ObjectId


class Master(BaseModel):
    id: Optional[str]
    type: Literal[
    "GENDER",
    "BLOOD_GRP",
    "MARITAL_STATUS",
    "LEAVE_TYPE"
    ]
    label: str
    value: str
    active: bool = True
