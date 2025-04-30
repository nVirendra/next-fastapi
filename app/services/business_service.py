from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import List, Optional
import re
from datetime import datetime


from app.core.config import MONGO_URI, DB_NAME
from app.schemas.business_schema import BusinessCreate, BusinessRead

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
business_collection = db["businesses"]

async def create_business(data: BusinessCreate) -> BusinessRead:
    existing = await business_collection.find_one({"email": data.email})
    if existing:
        raise HTTPException(status_code=400, detail="Business email already exists")

    data_dict = data.dict()
    data_dict["createdAt"] = datetime.utcnow()
    data_dict["updatedAt"] = datetime.utcnow()

    # Convert IDs to ObjectId for Mongo
    data_dict["business_type"] = ObjectId(data_dict["business_type"])
    data_dict["business_category"] = ObjectId(data_dict["business_category"])
    data_dict["address"]["country"] = ObjectId(data_dict["address"]["country"])
    
    result = await business_collection.insert_one(data_dict)
    data_dict["id"] = str(result.inserted_id)
    return BusinessRead(**data_dict)


async def get_businesses(skip: int = 0, limit: int = 10, search: Optional[str] = None) -> List[BusinessRead]:
    query = {}
    if search:
        regex = {"$regex": re.escape(search), "$options": "i"}
        query["$or"] = [{"name": regex}, {"email": regex}]

    cursor = business_collection.find(query).skip(skip).limit(limit)
    records = await cursor.to_list(length=limit)
    return [
        BusinessRead(
            id=str(b["_id"]),
            name=b["name"],
            email=b["email"],
            phone=b.get("phone"),
            address=b.get("address"),
            active=b.get("active", True)
        ) for b in records
    ]


async def get_business_by_id(business_id: str) -> Optional[BusinessRead]:
    b = await business_collection.find_one({"_id": ObjectId(business_id)})
    if b:
        return BusinessRead(
            id=str(b["_id"]),
            name=b["name"],
            email=b["email"],
            phone=b.get("phone"),
            address=b.get("address"),
            active=b.get("active", True)
        )
    return None


async def update_business(business_id: str, data: BusinessCreate) -> Optional[BusinessRead]:
    result = await business_collection.update_one(
        {"_id": ObjectId(business_id)},
        {"$set": data.dict()}
    )
    if result.matched_count == 0:
        return None
    return await get_business_by_id(business_id)


async def delete_business(business_id: str) -> bool:
    result = await business_collection.delete_one({"_id": ObjectId(business_id)})
    return result.deleted_count == 1
