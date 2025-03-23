from pydantic import BaseModel
from typing import Optional
from bson import ObjectId


class Menu(BaseModel):
    id: Optional[str]
    name: str                      # Display name of the menu
    slug: str                      # URL-friendly identifier
    icon: Optional[str] = None     # Icon name or identifier
    path: str                      # Route path (e.g. /dashboard/attendance)
    module: Optional[str] = None   # Link to associated module (if any)
    parent_id: Optional[str] = None  # For submenus
    active: bool = True
