import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost/tiktok_db"
    DATABASE_URL_MYSQL: str = "mysql+pymysql://tiktok_trends:tiktok_trends@194.164.126.55/tiktok_trends"
    DATABASE_TYPE: str = "mysql"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-this-in-production-tiktok-trends-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TikTok Database API"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080", "http://localhost:8000"]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"
    }


settings = Settings()
