from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class Settings(BaseSettings):
    """Load settings from .env file"""
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost/study_planner"
    )
    
    # JWT
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "dev-secret-key-change-in-production"
    )
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    
    # CORS (for frontend)
    ALLOWED_ORIGINS: list = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://study-planner-chi-smoky.vercel.app",  # ← YOUR EXACT URL
]
    
    class Config:
        env_file = ".env"


settings = Settings()