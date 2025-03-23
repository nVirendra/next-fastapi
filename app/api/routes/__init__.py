from fastapi import APIRouter
from app.api.routes.v1 import routers as v1_routers

api_router = APIRouter(prefix="/api/v1")

for router in v1_routers:
    api_router.include_router(router)
