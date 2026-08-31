from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models import Base

# Using SQLite for simplicity and easy deployment
DATABASE_URL = "sqlite+aiosqlite:///./bot_database.db"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_models():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
