from fastapi import APIRouter

from apis.users.routers import router as user_router
from apis.candlesticks.routers import router as candlestick_router
from apis.login.routers import router as login_router

api_router = APIRouter()

api_router.include_router(user_router, tags=["Users"], prefix="/users")
api_router.include_router(candlestick_router, tags=["Candlesticks"], prefix="/candlesticks")
api_router.include_router(login_router, tags=["Login"], prefix="/login")