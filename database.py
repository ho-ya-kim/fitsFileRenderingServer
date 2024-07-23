import asyncio

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, async_scoped_session

ASYNC_DB_INFO = {"host": "localhost",
                 "port": 3306,
                 "db": "fits",
                 "user": "root",
                 "passwd": "dlQmstjgh1!^^"}


def db_async_connection_sqlalchemy(db_info: dict) -> AsyncEngine:
    user = db_info['user']
    passwd = db_info['passwd']
    host = db_info['host']
    port = db_info['port']
    db = db_info['db']

    db_connections = f'mysql+aiomysql://{user}:{passwd}@{host}:{port}/{db}'
    engine = create_async_engine(db_connections, pool_recycle=600)

    return engine


async_engine = db_async_connection_sqlalchemy(ASYNC_DB_INFO)

Base = declarative_base()


async def get_async_db():
    db = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    async_session = async_scoped_session(db, scopefunc=asyncio.current_task)
    async with async_session() as session:
        yield session
