from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

sqlite_file_name = "database.sqlite"
sqlite_url = f"sqlite+aiosqlite:///{sqlite_file_name}"
engine = create_async_engine(sqlite_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def create_db_and_tables():
    async with engine.begin():
        pass
