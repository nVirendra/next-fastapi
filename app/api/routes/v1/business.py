from fastapi import APIRouter, HTTPException
from app.services.business_service import (
    create_business,
    get_businesses,
    get_business_by_id,
    update_business,
    delete_business
)

router = APIRouter(prefix="/businesses", tags=["Businesses"])

@router.post("/", response_model=BusinessRead, status_code=201)
async def create(data: BusinessCreate):
    return await create_business(data)

@router.get("/", response_model=List[BusinessRead])
async def read_all(
    skip: int = 0,
    limit: int = 20,
    search: Optional[str] = Query(None, description="Search by name or email")
):
    return await get_businesses(skip=skip, limit=limit, search=search)

@router.get("/{business_id}", response_model=BusinessRead)
async def read_one(business_id: str):
    business = await get_business_by_id(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business

@router.put("/{business_id}", response_model=BusinessRead)
async def update(business_id: str, data: BusinessCreate):
    updated = await update_business(business_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Business not found")
    return updated

@router.delete("/{business_id}")
async def delete(business_id: str):
    deleted = await delete_business(business_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Business not found")
    return {"message": "Business deleted successfully"}
