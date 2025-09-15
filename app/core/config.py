from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://user:password@localhost/tiktok_db"
    DATABASE_URL_MYSQL: str = "mysql+pymysql://tiktok_trends:tiktok_trends@194.164.126.55/tiktok_trends"
    DATABASE_TYPE: str = "mysql"  # postgresql or mysql
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "TikTok Database API"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8000",
        "http://localhost:5173",  # Vite dev server
    ]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


# Create settings instance
settings = Settings()
