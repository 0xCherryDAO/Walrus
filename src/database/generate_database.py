from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from loguru import logger

from src.database.base_models.pydantic_manager import DataBaseManagerConfig
from src.database.models import WorkingWallets, WalletsTasks
from src.database.utils.db_manager import DataBaseUtils
from config import *


async def clear_database(engine) -> None:
    async with AsyncSession(engine) as session:
        async with session.begin():
            for model in [WorkingWallets, WalletsTasks]:
                await session.execute(delete(model))
            await session.commit()
    logger.info("The database has been cleared")


async def generate_database(
        engine,
        mnemonics: list[str],
        proxies: list[str],
) -> None:
    await clear_database(engine)
    tasks = []
    if WITHDRAW_FROM_OKX:
        tasks.append('WITHDRAW_FROM_OKX')
    if FAUCET:
        tasks.append('FAUCET')
    if SWAP:
        tasks.append('SWAP')
    if STAKE:
        tasks.append('STAKE')
    if MINT_FLATLAND_NFT:
        tasks.append('MINT_FLATLAND_NFT')
    if BUY_WALRUS_NFT:
        tasks.append('BUY_NFT')

    proxy_index = 0
    for mnemonic in mnemonics:
        proxy = proxies[proxy_index]
        proxy_index = (proxy_index + 1) % len(proxies)

        proxy_url = None
        change_link = ''
        if proxy:
            if MOBILE_PROXY:
                proxy_url, change_link = proxy.split('|')
            else:
                proxy_url = proxy

        db_utils = DataBaseUtils(
            manager_config=DataBaseManagerConfig(
                action='working_wallets'
            )
        )

        await db_utils.add_to_db(
            mnemonic=mnemonic,
            proxy=f'{proxy_url}|{change_link}' if MOBILE_PROXY else proxy_url,
            recipient=None,
            status='pending',
        )
        for task in tasks:
            db_utils = DataBaseUtils(
                manager_config=DataBaseManagerConfig(
                    action='wallets_tasks'
                )
            )
            await db_utils.add_to_db(
                mnemonic=mnemonic,
                status='pending',
                task_name=task
            )
