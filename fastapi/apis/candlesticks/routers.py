from fastapi import APIRouter, Request
from fastapi.params import Depends
from fastapi_limiter.depends import RateLimiter
from fastapi_cache.decorator import cache

router = APIRouter()

@cache()
async def get_cache():
    return 1

@router.get("/", response_description="List all candlesticks data")
async def list_candlesticks(request: Request):
    result = request.app.clickhouse_client.execute("select * from data order by time desc limit 500")

    return result

@cache(expire=60)
@router.get("/withrediscache", response_description="Same data but with Redis cache that expires after 60 seconds")
async def list_candlesticks(request: Request):
    result = request.app.clickhouse_client.execute("select * from data order by time desc limit 500")

    return result

@router.get("/withratelimit", dependencies=[Depends(RateLimiter(times=1, seconds=5))], response_description="Same data but limited to 1 request every 5 seconds")
async def list_candlesticks_limited(request: Request):
    result = request.app.clickhouse_client.execute("select * from data order by time desc limit 500")

    return result