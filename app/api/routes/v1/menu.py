from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional

from app.schemas.menu_schema import MenuCreate, MenuRead
from app.services.menu_service import (
    create_menu,
    get_menus,
    get_menu_by_id,
    update_menu,
    delete_menu
)

router = APIRouter(prefix="/menus", tags=["Menus"])


@router.post("/", response_model=MenuRead, status_code=201)
async def create(data: MenuCreate):
    return await create_menu(data)


@router.get("/", response_model=List[MenuRead])
async def read_all(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = Query(None, description="Search by name or slug")
):
    return await get_menus(skip=skip, limit=limit, search=search)


@router.get("/{menu_id}", response_model=MenuRead)
async def read_one(menu_id: str):
    menu = await get_menu_by_id(menu_id)
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")
    return menu


@router.put("/{menu_id}", response_model=MenuRead)
async def update(menu_id: str, data: MenuCreate):
    updated = await update_menu(menu_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Menu not found")
    return updated


@router.delete("/{menu_id}")
async def delete(menu_id: str):
    deleted = await delete_menu(menu_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Menu not found")
    return {"message": "Menu deleted successfully"}
