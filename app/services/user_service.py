
from app.schemas.user import UserCreate, UserRead
from app.core.config import MONGO_URI, DB_NAME
from pymongo import MongoClient
from bson import ObjectId


client = MongoClient(MONGO_URI)
db = client[DB_NAME]
user_collection = db["users"]

def create_user(user: UserCreate) -> UserRead:
    user_dict = user.dict()
    result = user_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return UserRead(**user_dict)

def get_users() -> list[UserRead]:
    users = user_collection.find()
    return [UserRead(id=str(u["_id"]), name=u["name"], email=u["email"]) for u in users]
