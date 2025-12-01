from logging.config import fileConfig

from alembic import context
from app.core.config import settings
from app.models import Base
from sqlalchemy import create_engine, pool

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def _sync_url_from_async(url: str) -> str:
    if "+asyncpg" in url:
        return url.replace("+asyncpg", "")
    # fallback: if url contains '+driver' for postgres, remove driver part
    if "+" in url and url.startswith("postgresql"):
        return url.split("+", 1)[0] + url.split(":", 1)[1]
    return url


def run_migrations_offline():
    sync_url = _sync_url_from_async(settings.DATABASE_URL)
    context.configure(
        url=sync_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    sync_url = _sync_url_from_async(settings.DATABASE_URL)
    connectable = create_engine(sync_url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
