from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional
import re

from app.core.config import MONGO_URI, DB_NAME
from app.schemas.user import UserCreate, UserRead

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
user_collection = db["users"]


async def create_user(user: UserCreate) -> UserRead:
    existing = await user_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user_dict = user.dict()
    result = await user_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    return UserRead(**user_dict)


async def get_users(skip: int = 0, limit: int = 10, search: Optional[str] = None) -> List[UserRead]:
    query = {}
    if search:
        regex = {"$regex": re.escape(search), "$options": "i"}
        query["$or"] = [{"name": regex}, {"email": regex}]

    cursor = user_collection.find(query).skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)

    return [
        UserRead(
            id=str(u["_id"]),
            name=u["name"],
            email=u["email"],
            first_name=u["first_name"],
            last_name=u["last_name"],
            role_id=u["role_id"],
            phone_no=u["phone_no"],
        )
        for u in users
    ]


async def get_user_by_id(user_id: str) -> Optional[UserRead]:
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return UserRead(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"]
        )
    return None


async def update_user(user_id: str, user: UserCreate) -> Optional[UserRead]:
    result = await user_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user.dict()}
    )
    if result.matched_count == 0:
        return None
    return await get_user_by_id(user_id)


async def delete_user(user_id: str) -> bool:
    result = await user_collection.delete_one({"_id": ObjectId(user_id)})
    return result.deleted_count == 1
