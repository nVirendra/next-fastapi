from app.schemas.menu_schema import MenuCreate, MenuRead

menu_collection = db["menus"]

async def create_menu(data: MenuCreate) -> MenuRead:
    existing = await menu_collection.find_one({"slug": data.slug})
    if existing:
        raise HTTPException(status_code=400, detail="Menu slug already exists")

    data_dict = data.dict()
    result = await menu_collection.insert_one(data_dict)
    data_dict["id"] = str(result.inserted_id)
    return MenuRead(**data_dict)


async def get_menus(skip: int = 0, limit: int = 10, search: Optional[str] = None) -> List[MenuRead]:
    query = {}
    if search:
        regex = {"$regex": re.escape(search), "$options": "i"}
        query["$or"] = [{"name": regex}, {"slug": regex}]

    cursor = menu_collection.find(query).skip(skip).limit(limit)
    records = await cursor.to_list(length=limit)
    return [
        MenuRead(
            id=str(m["_id"]),
            name=m["name"],
            slug=m["slug"],
            icon=m.get("icon"),
            path=m["path"],
            module=m.get("module"),
            parent_id=m.get("parent_id"),
            active=m.get("active", True)
        ) for m in records
    ]


async def get_menu_by_id(menu_id: str) -> Optional[MenuRead]:
    menu = await menu_collection.find_one({"_id": ObjectId(menu_id)})
    if menu:
        return MenuRead(
            id=str(menu["_id"]),
            name=menu["name"],
            slug=menu["slug"],
            icon=menu.get("icon"),
            path=menu["path"],
            module=menu.get("module"),
            parent_id=menu.get("parent_id"),
            active=menu.get("active", True)
        )
    return None


async def update_menu(menu_id: str, data: MenuCreate) -> Optional[MenuRead]:
    result = await menu_collection.update_one(
        {"_id": ObjectId(menu_id)},
        {"$set": data.dict()}
    )
    if result.matched_count == 0:
        return None
    return await get_menu_by_id(menu_id)


async def delete_menu(menu_id: str) -> bool:
    result = await menu_collection.delete_one({"_id": ObjectId(menu_id)})
    return result.deleted_count == 1

