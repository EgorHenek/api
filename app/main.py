from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.db import database
from app.meilisearch import meilisearch_client
from app.routers import (
    comments,
    djs,
    livestreams,
    posts,
    tokens,
    upload,
    users,
    videos,
)
from app.settings import settings

openapi_url = "/openapi.json" if settings.debug else None
app = FastAPI(openapi_url=openapi_url, debug=settings.debug)


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()
    await meilisearch_client.close()


origins = ["https://edm.su", "http://localhost:3000"]

app.include_router(videos.router)
app.include_router(tokens.router)
app.include_router(users.router)
app.include_router(comments.router)
app.include_router(posts.router)
app.include_router(upload.router)
app.include_router(livestreams.router)
app.include_router(djs.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["x-total-count"],
)
