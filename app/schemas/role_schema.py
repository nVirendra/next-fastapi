class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None
    active: bool = True

class RoleRead(RoleCreate):
    id: str