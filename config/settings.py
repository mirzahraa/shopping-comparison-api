from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    SECRET_KEY: str = "your-secret-key-change-in-production"
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/shopping_comparison_db"
    MONGODB_URL: str = "mongodb://localhost:27017/shopping_comparison"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # API Keys
    AMAZON_API_KEY: Optional[str] = None
    FLIPKART_API_KEY: Optional[str] = None
    MYNTRA_API_KEY: Optional[str] = None
    REDTAPE_API_KEY: Optional[str] = None
    VMART_API_KEY: Optional[str] = None
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # Scraping
    SCRAPER_USER_AGENT: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    SCRAPER_TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    RATE_LIMIT_DELAY: int = 2
    
    # Cache
    CACHE_TTL: int = 3600
    PRICE_UPDATE_INTERVAL: int = 3600
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()