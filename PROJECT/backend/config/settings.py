"""
Configuration settings for the Automated Failure Attribution Engine.
"""
from typing import Optional, Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # Application Config
    APP_NAME: str = "Automated Failure Attribution Engine"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    
    # LLM Judge Configuration
    # Supported providers: "mock", "ollama", "vllm", "openai", "gemini", "groq"
    LLM_PROVIDER: str = "mock"
    LLM_MODEL: str = "Qwen/Qwen2.5-7B-Instruct"
    LLM_BASE_URL: Optional[str] = "http://localhost:8000/v1"
    LLM_API_KEY: Optional[str] = None
    LLM_TEMPERATURE: float = 0.0
    LLM_MAX_TOKENS: int = 1024
    LLM_TIMEOUT_SECONDS: int = 60
    
    # Caching & Storage Settings
    CACHE_ENABLED: bool = True
    CACHE_BACKEND: Literal["sqlite", "mongodb", "redis", "memory"] = "sqlite"
    SQLITE_DB_PATH: str = str(BASE_DIR / "cache.db")
    MONGODB_URI: str = "mongodb://localhost:27017"
    MONGODB_DB_NAME: str = "failure_attribution"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Celery Task Queue
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/1"
    
    # Token Context Limits (for segmentation)
    MAX_TURN_TOKENS: int = 4096
    MAX_TRACE_CONTEXT_TOKENS: int = 32768
    
    # Dataset Paths
    DATASET_DIR: Path = BASE_DIR / "dataset" / "data"
    
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
