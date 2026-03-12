from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.app.api.v1.auth.router import router as auth_router
from backend.app.core.db import init_db
from backend.app.api.v1.posts.router import router as posts_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    lifespan=lifespan
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(posts_router, prefix="/api/v1")
