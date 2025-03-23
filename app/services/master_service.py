from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional
import re

from app.core.config import MONGO_URI, DB_NAME
from app.schemas.master_schema import MasterCreate, MasterRead

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
master_collection = db["masters"]

async def create_master(data: MasterCreate) -> MasterRead:
    existing = await master_collection.find_one({
        "type": data.type,
        "value": data.value
    })
    if existing:
        raise HTTPException(status_code=400, detail="Master entry already exists")

    data_dict = data.dict()
    result = await master_collection.insert_one(data_dict)
    data_dict["id"] = str(result.inserted_id)
    return MasterRead(**data_dict)


async def get_masters(skip: int = 0, limit: int = 10, search: Optional[str] = None, type: Optional[str] = None) -> List[MasterRead]:
    query = {}
    if search:
        regex = {"$regex": re.escape(search), "$options": "i"}
        query["$or"] = [{"label": regex}, {"value": regex}]
    if type:
        query["type"] = type

    cursor = master_collection.find(query).skip(skip).limit(limit)
    records = await cursor.to_list(length=limit)
    return [
        MasterRead(
            id=str(m["_id"]),
            type=m["type"],
            label=m["label"],
            value=m["value"],
            active=m.get("active", True)
        ) for m in records
    ]


async def get_master_by_id(master_id: str) -> Optional[MasterRead]:
    master = await master_collection.find_one({"_id": ObjectId(master_id)})
    if master:
        return MasterRead(
            id=str(master["_id"]),
            type=master["type"],
            label=master["label"],
            value=master["value"],
            active=master.get("active", True)
        )
    return None


async def update_master(master_id: str, data: MasterCreate) -> Optional[MasterRead]:
    result = await master_collection.update_one(
        {"_id": ObjectId(master_id)},
        {"$set": data.dict()}
    )
    if result.matched_count == 0:
        return None
    return await get_master_by_id(master_id)


async def delete_master(master_id: str) -> bool:
    result = await master_collection.delete_one({"_id": ObjectId(master_id)})
    return result.deleted_count == 1