from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Chat Server"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/aiserver")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000", "http://10.0.0.42:3000"]
    
    # AI Model Settings
    MODEL_NAME: str = "microsoft/Phi-4-reasoning-plus"  # 使用Phi-4-reasoning-plus模型
    MODEL_DEVICE: str = "cuda"  # 使用GPU
    MAX_LENGTH: int = 2048
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.95
    TOP_K: int = 50
    
    class Config:
        case_sensitive = True

settings = Settings() 