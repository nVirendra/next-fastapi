from fastapi import FastAPI
from app.api.routes import user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
