
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


def get_user_by_id(user_id: str) -> UserRead | None:
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return UserRead(id=str(user["_id"]), name=user["name"], email=user["email"])
    return None


def update_user(user_id: str, user: UserCreate) -> UserRead | None:
    result = user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user.dict()}
    )
    if result.matched_count == 0:
        return None
    return get_user_by_id(user_id)

def delete_user(user_id: str) -> bool:
    result = user_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count == 1