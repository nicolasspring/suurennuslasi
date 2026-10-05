from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from suurennuslasi_db.session.config import settings

engine = create_async_engine(
    settings.SUURENNUSLASI_DATABASE_URL,
    echo=settings.SUURENNUSLASI_DB_ECHO,
    pool_size=settings.SUURENNUSLASI_DB_POOL_SIZE,
    max_overflow=settings.SUURENNUSLASI_DB_MAX_OVERFLOW,
    pool_timeout=settings.SUURENNUSLASI_DB_POOL_TIMEOUT,
    pool_recycle=settings.SUURENNUSLASI_DB_POOL_RECYCLE,
    pool_pre_ping=True,
    connect_args={
        "timeout": settings.SUURENNUSLASI_DB_CONNECT_TIMEOUT,
        "command_timeout": settings.SUURENNUSLASI_DB_COMMAND_TIMEOUT,
    },
)


AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
