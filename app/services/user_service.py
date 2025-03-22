from app.schemas.user import UserCreate, UserRead
from app.core.config import MONGO_URI, DB_NAME
from pymongo import MongoClient
from bson import ObjectId, Regex
from typing import List, Optional
import re

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
user_collection = db["users"]

def create_user(user: UserCreate) -> UserRead:
    user_dict = user.dict()
    result = user_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return UserRead(**user_dict)

def get_users(skip: int = 0, limit: int = 10, search: Optional[str] = None) -> List[UserRead]:
    query = {}
    if search:
        regex = {"$regex": re.escape(search), "$options": "i"}  # case-insensitive
        query = {"$or": [{"name": regex}, {"email": regex}]}

    users = user_collection.find(query).skip(skip).limit(limit)
    return [UserRead(id=str(u["_id"]), name=u["name"], email=u["email"]) for u in users]

def get_user_by_id(user_id: str) -> Optional[UserRead]:
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return UserRead(id=str(user["_id"]), name=user["name"], email=user["email"])
    return None

def update_user(user_id: str, user: UserCreate) -> Optional[UserRead]:
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
