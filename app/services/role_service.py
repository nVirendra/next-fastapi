from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional
import re

from app.core.config import MONGO_URI, DB_NAME
from app.schemas.role_schema import RoleCreate, RoleRead

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
role_collection = db["roles"]

async def create_role(data: RoleCreate) -> RoleRead:
    existing = await role_collection.find_one({"name": data.name})
    if existing:
        raise HTTPException(status_code=400, detail="Role name already exists")

    data_dict = data.dict()
    result = await role_collection.insert_one(data_dict)
    data_dict["id"] = str(result.inserted_id)
    return RoleRead(**data_dict)


async def get_roles(skip: int = 0, limit: int = 10, search: Optional[str] = None) -> List[RoleRead]:
    query = {}
    if search:
        regex = {"$regex": re.escape(search), "$options": "i"}
        query["name"] = regex

    cursor = role_collection.find(query).skip(skip).limit(limit)
    records = await cursor.to_list(length=limit)
    return [
        RoleRead(
            id=str(r["_id"]),
            name=r["name"],
            description=r.get("description"),
            active=r.get("active", True)
        ) for r in records
    ]


async def get_role_by_id(role_id: str) -> Optional[RoleRead]:
    role = await role_collection.find_one({"_id": ObjectId(role_id)})
    if role:
        return RoleRead(
            id=str(role["_id"]),
            name=role["name"],
            description=role.get("description"),
            active=role.get("active", True)
        )
    return None


async def update_role(role_id: str, data: RoleCreate) -> Optional[RoleRead]:
    result = await role_collection.update_one(
        {"_id": ObjectId(role_id)},
        {"$set": data.dict()}
    )
    if result.matched_count == 0:
        return None
    return await get_role_by_id(role_id)


async def delete_role(role_id: str) -> bool:
    result = await role_collection.delete_one({"_id": ObjectId(role_id)})
    return result.deleted_count == 1
