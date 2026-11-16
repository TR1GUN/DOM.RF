from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from settings.settings import settings_app


def _get_database_url() -> str:
    """Construct PostgreSQL database URL from settings."""
    return (
        f"postgresql+asyncpg://{settings_app.database.db_user}:"
        f"{settings_app.database.db_password}@"
        f"{settings_app.database.db_host}:{settings_app.database.db_port}/"
        f"{settings_app.database.db_database}"
    )


class DataBaseManager:
    """Database manager for handling SQLAlchemy async sessions."""

    def __init__(self):
        self.engine = create_async_engine(
            _get_database_url(),
            echo=False,  # Set to True for SQL query logging
            pool_pre_ping=True,  # Verify connections before use
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

    async def session_dependency(self) -> AsyncSession:
        """FastAPI dependency for unscoped session."""
        async with self.session_factory() as session:
            yield session

    async def scoped_session_dependency(self) -> AsyncSession:
        """FastAPI dependency for scoped session.
        Creates a new session per request, closes it after.
        """
        async with self.session_factory() as session:
            yield session
