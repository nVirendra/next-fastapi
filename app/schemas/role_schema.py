from app.db.models.role_model import Role

class RoleCreate(Role):
    pass

class RoleRead(Role):
    id: str
