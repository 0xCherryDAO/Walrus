import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from sqlalchemy import (
    Sequence,
    Integer,
    Column,
    String,
)

Base = declarative_base()


class WorkingWallets(Base):
    __tablename__ = 'working_wallets'
    id = Column(Integer, Sequence('working_wallets_id_seq'), primary_key=True)
    mnemonic = Column(String)
    proxy = Column(String, nullable=True)
    recipient = Column(String, nullable=True)
    status = Column(String)


class WalletsTasks(Base):
    __tablename__ = 'wallets_tasks'

    id = Column(Integer, Sequence('wallets_tasks_id_seq'), primary_key=True)
    mnemonic = Column(String, unique=False)
    task_name = Column(String, unique=False)
    status = Column(String, unique=False)


logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

engine = create_async_engine(
    'sqlite+aiosqlite:///transactions.db',
    echo=False
)


async def init_models(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
