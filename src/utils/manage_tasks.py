from src.database.base_models.pydantic_manager import DataBaseManagerConfig
from src.database.utils.db_manager import DataBaseUtils


async def manage_tasks(mnemonic: str, task: str) -> None:
    db_utils = DataBaseUtils(
        manager_config=DataBaseManagerConfig(
            action='wallets_tasks'
        )
    )

    await db_utils.add_to_db(
        mnemonic=mnemonic,
        task_name=task,
        status='completed'
    )
