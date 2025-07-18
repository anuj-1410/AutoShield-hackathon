"""
AutoShield Backend Configuration
Environment-based configuration management
"""

import os
from functools import lru_cache
from typing import List, Optional
from pydantic import BaseSettings, validator
from pydantic_settings import BaseSettings as PydanticSettings

class Settings(PydanticSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Application
    APP_NAME: str = "AutoShield"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://autoshield:password@localhost:5432/autoshield"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    REDIS_EXPIRE_TIME: int = int(os.getenv("REDIS_EXPIRE_TIME", "3600"))
    
    # Blockchain
    BLOCKCHAIN_RPC_URL: str = os.getenv(
        "BLOCKCHAIN_RPC_URL", 
        "http://localhost:8545"
    )
    CONTRACT_ADDRESS: str = os.getenv("CONTRACT_ADDRESS", "")
    PRIVATE_KEY: str = os.getenv("PRIVATE_KEY", "")
    
    # AI/ML
    AI_MODEL_PATH: str = os.getenv("AI_MODEL_PATH", "/app/models")
    AI_CONFIDENCE_THRESHOLD: float = float(os.getenv("AI_CONFIDENCE_THRESHOLD", "0.7"))
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "https://localhost:3000",
        "http://127.0.0.1:3000",
        "https://autoshield.app"
    ]
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))
    
    # Security Headers
    ALLOWED_HOSTS: List[str] = [
        "localhost",
        "127.0.0.1",
        "autoshield.app",
        "api.autoshield.app"
    ]
    
    # External Services
    IPFS_GATEWAY: str = os.getenv("IPFS_GATEWAY", "https://ipfs.io/ipfs/")
    IPFS_API_URL: str = os.getenv("IPFS_API_URL", "http://localhost:5001")
    
    # Monitoring
    SENTRY_DSN: Optional[str] = os.getenv("SENTRY_DSN")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Email (for notifications)
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM: str = os.getenv("EMAIL_FROM", "noreply@autoshield.app")
    
    # File Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/app/uploads")
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    
    # API Keys for external services
    ETHERSCAN_API_KEY: str = os.getenv("ETHERSCAN_API_KEY", "")
    MORALIS_API_KEY: str = os.getenv("MORALIS_API_KEY", "")
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @validator("ALLOWED_HOSTS", pre=True)
    def assemble_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance
    """
    return Settings()
