from app.models import verify_password
from app.auth import create_access_token
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional
import re


from app.core.config import MONGO_URI, DB_NAME
from app.schemas.clt_user_schema import UserRead,TokenResponse

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
user_collection = db["clt_users"]


async def get_users( current_user: dict = None, skip: int = 0, limit: int = 10, search: Optional[str] = None) -> List[UserRead]:
    query = {}
    if search:
        regex = {"$regex": re.escape(search), "$options": "i"}
        query["$or"] = [{"name": regex}, {"email": regex}]

    # Example: You can use current_user if needed (like filtering or logging)
    print(f"Fetching users for logged-in user: {current_user['email']}")
    cursor = user_collection.find(query).skip(skip).limit(limit)
    users = await cursor.to_list(length=limit)
    return [
        UserRead(
            id=str(u["_id"]),
            user_id=u["user_id"],
            username=u["username"],
            name=u["name"],
            email=u["email"],
            country=u["country"],
            join_date=u["join_date"],
            gender=u["gender"],
            age=u["age"],
            hobbies=u["hobbies"],
            education=u["education"],
        )
        for u in users
    ]


async def login_user(email: str, password: str):
    user = await user_collection.find_one({"email": email})

    if not user or "hashed_password" not in user:
        return None

    if not verify_password(password, user["hashed_password"]):
        return None

    access_token = create_access_token(data={"sub": str(user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}

   