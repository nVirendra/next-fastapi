from pydantic import BaseModel
from typing import Literal

# Expanded master types
MasterType = Literal[
    "GENDER",
    "BLOOD_GRP",
    "MARITAL_STATUS",
    "LEAVE_TYPE"
]

class MasterCreate(BaseModel):
    type: MasterType
    label: str
    value: str
    active: bool = True

class MasterRead(MasterCreate):
    id: str
