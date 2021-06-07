import os
from pydantic import BaseSettings

class CommonSettings(BaseSettings):
    PROJECT_TITLE: str = "Demo API"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_DESCRIPTION: str = "Demo API with a modern backend stack."
    PROJECT_METADATA: list = [
        {
            "name": "Users",
            "description": "Users Endpoint based on MongoDB",
        },
        {
            "name": "Candlesticks",
            "description": "Candlesticks Endpoint based on Clickhouse",
            "externalDocs": {
                "description": "Source",
                "url": "https://www.cryptodatadownload.com/",
            },
        },
        {
            "name": "Login",
            "description": "Login with JSON Web Tokens",
            "externalDocs": {
                "description": "Documentation",
                "url": "https://jwt.io/",
            },
        },
    ]

class DatabaseSettings(BaseSettings):
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    CLICKHOUSE_URL: str = os.getenv("CLICKHOUSE_URL", "clickhouse+native://localhost")
    REDIS_URL: str = os.getenv("CLICKHOUSE_URL", "redis://localhost")

class SecuritySettings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

class TestingSettings(BaseSettings):
    USERNAME: str = "demo"
    PASSWORD: str = "demo"

class Settings(CommonSettings, DatabaseSettings, SecuritySettings, TestingSettings):
    pass

settings = Settings()