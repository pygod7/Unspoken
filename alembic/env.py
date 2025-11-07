import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from alembic import context

# Import your Base and models
from app.database.models import Base  # adjust path if needed
from app.settings import Settings      # to read DATABASE_URL from .env

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# SQLAlchemy URL
settings = Settings()
DATABASE_URL = settings.DATABASE_URL

# target_metadata is used by 'autogenerate' to detect schema changes
target_metadata = Base.metadata

# ---------------------------------------------------------------------
# Offline migrations (generates SQL scripts)
# ---------------------------------------------------------------------
def run_migrations_offline():
    url = DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------
# Online migrations (applies to live DB)
# ---------------------------------------------------------------------
def run_migrations_online():
    """Run migrations using an async engine."""

    connectable = create_async_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
        future=True,
    )

    async def do_run_migrations():
        async with connectable.connect() as connection:
            # run_sync allows sync migration logic (do_run_migrations) to run on async connection
            await connection.run_sync(do_run_migrations_sync)

    # Sync migration logic
    def do_run_migrations_sync(connection: Connection):
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

    asyncio.run(do_run_migrations())


# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
