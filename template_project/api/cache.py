from typing import Any, Callable, Dict, Tuple

from fastapi import Request, Response
from fastapi_cache import FastAPICache
from fastapi_cache.backends import Backend
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from template_project.config import CacheSettings


def request_key_builder(
    func: Callable[..., Any],
    namespace: str = "",
    *,
    request: Request | None = None,
    response: Response | None = None,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
):
    """
    https://github.com/long2ice/fastapi-cache?tab=readme-ov-file#custom-key-builder
    """

    key = ":".join(
        [
            FastAPICache.get_prefix(),
            namespace,
            request.method.lower(),
            request.url.path,
            repr(sorted(request.query_params.items())),
        ]
    )
    return key


def get_cache_backend(backend: str, connection_string: str | None) -> Backend:
    if backend == 'redis':
        redis = aioredis.from_url(connection_string)
        return RedisBackend(redis)
    else:
        return InMemoryBackend()


def initialise_cache():
    cache_config = CacheSettings()

    backend = get_cache_backend(cache_config.BACKEND, cache_config.CONNECTION_STRING)
    FastAPICache.init(
        backend=backend,
        expire=cache_config.EXPIRATION,
        prefix=cache_config.PREFIX,
        key_builder=request_key_builder,
        enable=cache_config.ENABLED,
    )
