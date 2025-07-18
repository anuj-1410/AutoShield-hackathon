"""
AutoShield Database Utility
SQLAlchemy Async ORM setup
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

# Get application settings
settings = get_settings()
DATABASE_URL = settings.DATABASE_URL

# Create async SQLAlchemy engine
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Create session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db() -> AsyncSession:
    """
    Provide a transactional scope around a series of operations
    """
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    """
    Initialize and setup the database
    """
    async with engine.begin() as conn:
        # Example: You can run migrations or any initialization logic here
        await conn.execute("SELECT 1")  # Test connection
        print("Database initialized.")
    
    print("Database connected successfully.")
