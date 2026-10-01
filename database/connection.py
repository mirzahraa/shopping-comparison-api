from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

# Database setup
engine = None
SessionLocal = None
Base = declarative_base()

async def init_db():
    """
    Initialize database connection.
    """
    global engine, SessionLocal
    try:
        engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            future=True,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
        SessionLocal = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Create tables
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {str(e)}")
        raise

async def get_db() -> AsyncSession:
    """
    Get database session.
    """
    if not SessionLocal:
        raise RuntimeError("Database not initialized")
    
    async with SessionLocal() as session:
        yield session

async def close_db():
    """
    Close database connection.
    """
    global engine
    if engine:
        await engine.dispose()
        logger.info("Database connection closed")