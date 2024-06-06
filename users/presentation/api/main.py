from contextlib import asynccontextmanager
import uvicorn
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from users.infrastructure.db.models import User
from presentation.api.config import api_settings

from presentation.api.controllers.user import router as user_router
from presentation.api.controllers.auth import router as auth_router
from presentation.api.middlewares.logging import RequestLogMiddleware

from users.config import settings


MIDDLEWARES = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
    Middleware(RequestLogMiddleware),
]


@asynccontextmanager
async def lifespan_init_db(app: FastAPI):
    client = AsyncIOMotorClient(str(settings.infrastructure.mongo_dsn))
    await init_beanie(database=client.chat, document_models=[User])
    yield


app = FastAPI(title="chat", version="1.0.0", middleware=MIDDLEWARES, lifespan=lifespan_init_db, debug=True)


ROUTERS = [
    user_router,
    auth_router,
]

for router in ROUTERS:
    app.include_router(router)


def main():
    uvicorn.run(
        "presentation.api.main:app",
        host=api_settings.HOST,
        port=api_settings.PORT,
        reload=api_settings.RELOAD,
        workers=api_settings.WORKERS,
        log_level="info",
    )


if __name__ == "__main__":
    main()