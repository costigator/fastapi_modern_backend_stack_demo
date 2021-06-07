import aioredis
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from clickhouse_driver import Client as ClickhouseClient
from fastapi_limiter import FastAPILimiter
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_fastapi_instrumentator import Instrumentator

from apis.base import api_router
from webapps.base import webapp_router

from config import settings

# FastAPI app
app = FastAPI(title=settings.PROJECT_TITLE,
              version=settings.PROJECT_VERSION,
              description=settings.PROJECT_DESCRIPTION,
              openapi_tags=settings.PROJECT_METADATA)

# Prometheus metrics
Instrumentator().instrument(app).expose(app, include_in_schema=False)

@app.on_event("startup")
async def startup_db_clients():

    # MongoDB with asynchronous code
    app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
    app.mongodb = app.mongodb_client["test"]

    # Clickhouse
    app.clickhouse_client = ClickhouseClient(settings.CLICKHOUSE_URL)

    # Redis cache
    redis = await aioredis.create_redis_pool(settings.REDIS_URL, encoding="utf8")
    await FastAPILimiter.init(redis)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    
@app.on_event("shutdown")
async def shutdown_db_clients():
    app.mongodb_client.close()
    app.clickhouse_client.disconnect()

app.include_router(api_router)
app.include_router(webapp_router)
