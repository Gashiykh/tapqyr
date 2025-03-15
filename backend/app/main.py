import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse


from app.core import settings, db_helper
from app.api import auth_router
from app.api import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    #startup
    yield
    #showdown
    await db_helper.dispose()

main_app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

main_app.include_router(
    auth_router,
    prefix='/auth',
    tags=['auth']
)
main_app.include_router(
    user_router,
    prefix='/user',
    tags=['user']
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )