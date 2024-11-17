from typing import List, Optional

from loguru import logger

from src.database.base_models.pydantic_manager import DataBaseManagerConfig
from src.database.utils.db_manager import DataBaseUtils
from src.models.route import Route, Wallet


async def get_routes(mnemonics: str) -> Optional[List[Route]]:
    db_utils = DataBaseUtils(
        manager_config=DataBaseManagerConfig(
            action='working_wallets'
        )
    )
    result = await db_utils.get_uncompleted_wallets()
    if not result:
        logger.success(f'Все кошельки с данной базы данных уже отработали')
        return

    routes = []
    for wallet in result:
        for mnemonic in mnemonics:
            if wallet.mnemonic.lower() == mnemonic.lower():
                private_key_tasks = await db_utils.get_wallet_pending_tasks(mnemonic)
                tasks = []
                for task in private_key_tasks:
                    tasks.append(task.task_name)
                routes.append(
                    Route(
                        tasks=tasks,
                        wallet=Wallet(
                            mnemonic=mnemonic,
                            recipient=wallet.recipient,
                            proxy=wallet.proxy,
                        )
                    )
                )
    return routes
