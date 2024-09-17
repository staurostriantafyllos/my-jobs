from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from template_project.api.cache import initialise_cache
from template_project.api.exceptions import EntityNotFoundException
from template_project.api.routers import accounts, system
from template_project.config import APISettings


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.deployed_at = datetime.now(timezone.utc)

    initialise_cache()
    yield


def entity_not_found_exception_handler(
    request: Request, exc: EntityNotFoundException
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Entity not found"}
    )


def create_api_application() -> FastAPI:
    api_config = APISettings()  # type: ignore

    if api_config.DOCS_ENABLED:
        docs_url = '/docs'
        redoc_url = '/redoc_url'
    else:
        docs_url = None
        redoc_url = None

    app = FastAPI(lifespan=lifespan, docs_url=docs_url, redoc_url=redoc_url)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=api_config.ORIGINS,
        allow_origin_regex=api_config.ORIGIN_REGEX,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # include routers here
    app.include_router(system.router)
    app.include_router(accounts.router)

    app.add_exception_handler(
        EntityNotFoundException, entity_not_found_exception_handler
    )

    return app
