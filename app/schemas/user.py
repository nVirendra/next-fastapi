
from app.db.models.user_model import User

class UserCreate(User):
    pass

class UserRead(User):
    id: str
