from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from .models import Base
import os

# Using /app/data if it exists (for Bothost persistence), else local file
db_path = "/app/data/bot_database.db" if os.path.isdir("/app/data") else "./bot_database.db"
DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_models():
    async with engine.begin() as conn:
        # Create tables
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
