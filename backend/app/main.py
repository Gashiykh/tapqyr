from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI

from app.core import settings, db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    yield
    #showdown
    await db_helper.dispose()

main_app = FastAPI(
    lifespan=lifespan,
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )