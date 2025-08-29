import os
from functools import lru_cache

from sqlalchemy.ext.asyncio import create_async_engine


@lru_cache
def create_db_engine():
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    db = os.environ["POSTGRES_DB"]
    host = os.environ["POSTGRES_HOST"]
    port = os.environ["POSTGRES_PORT"]
    db_url = f"postgresql+psycopg://{user}:{password}@{host}:{port}/{db}"

    db_engine = create_async_engine(db_url)
    return db_engine