from app.schemas.module_schema import ModuleCreate, ModuleRead

module_collection = db["modules"]

async def create_module(data: ModuleCreate) -> ModuleRead:
    existing = await module_collection.find_one({"slug": data.slug})
    if existing:
        raise HTTPException(status_code=400, detail="Module slug already exists")

    data_dict = data.dict()
    result = await module_collection.insert_one(data_dict)
    data_dict["id"] = str(result.inserted_id)
    return ModuleRead(**data_dict)


async def get_modules(skip: int = 0, limit: int = 10, search: Optional[str] = None) -> List[ModuleRead]:
    query = {}
    if search:
        regex = {"$regex": re.escape(search), "$options": "i"}
        query["$or"] = [
            {"name": regex},
            {"slug": regex},
            {"description": regex}
        ]

    cursor = module_collection.find(query).skip(skip).limit(limit)
    records = await cursor.to_list(length=limit)
    return [
        ModuleRead(
            id=str(m["_id"]),
            name=m["name"],
            slug=m["slug"],
            description=m.get("description"),
            features=m.get("features", []),
            monthly_price=m["monthly_price"],
            yearly_price=m["yearly_price"],
            active=m.get("active", True)
        ) for m in records
    ]


async def get_module_by_id(module_id: str) -> Optional[ModuleRead]:
    module = await module_collection.find_one({"_id": ObjectId(module_id)})
    if module:
        return ModuleRead(
            id=str(module["_id"]),
            name=module["name"],
            slug=module["slug"],
            description=module.get("description"),
            features=module.get("features", []),
            monthly_price=module["monthly_price"],
            yearly_price=module["yearly_price"],
            active=module.get("active", True)
        )
    return None


async def update_module(module_id: str, data: ModuleCreate) -> Optional[ModuleRead]:
    result = await module_collection.update_one(
        {"_id": ObjectId(module_id)},
        {"$set": data.dict()}
    )
    if result.matched_count == 0:
        return None
    return await get_module_by_id(module_id)


async def delete_module(module_id: str) -> bool:
    result = await module_collection.delete_one({"_id": ObjectId(module_id)})
    return result.deleted_count == 1