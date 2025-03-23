from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.v1 import user, master, menu, module

app = FastAPI(title="HRMS Super Admin API", version="1.0.0")

# Mount versioned API routers
app.include_router(user.router, prefix="/api/v1")
app.include_router(master.router, prefix="/api/v1")
app.include_router(menu.router, prefix="/api/v1")
app.include_router(module.router, prefix="/api/v1")

#  CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Optional: health check
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}
