from fastapi import APIRouter, Depends, Query, Request
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from template_project.api.auth import verify_api_token

router = APIRouter(
    prefix="",
    tags=["system"],
)


@router.get("/health")
def health(request: Request) -> dict:
    return {
        "status": "ok",
        "deployed_at": request.app.state.deployed_at.isoformat(),
        "version": "0.0.1",
    }


@router.get("/clear-cache")
async def clear(
    namespace: str = Query(None),
    _: dict = Depends(verify_api_token),
):
    return await FastAPICache.clear(namespace)


@router.get("/cache-info")
async def cache_info(_: dict = Depends(verify_api_token)) -> dict:
    backend = FastAPICache.get_backend()

    info = None
    if isinstance(backend, RedisBackend):
        info = await backend.redis.info()

    return {
        'prefix': FastAPICache.get_prefix(),
        'enabled': FastAPICache.get_enable(),
        'expiration': FastAPICache.get_expire(),
        'cache_info': info,
    }
