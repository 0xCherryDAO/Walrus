from src.database.base_models.pydantic_manager import DataBaseManagerConfig
from src.database.utils.db_manager import DataBaseUtils
from src.utils.request_client.client import RequestClient
from src.utils.user.sui_account import SuiAccount


class TGApp(RequestClient):
    def __init__(
            self,
            token: str,
            tg_id: int,
            mnemonic: str,
    ):
        self.mnemonic = mnemonic
        self.__account = SuiAccount(
            mnemonic=mnemonic
        )

        self.token = token
        self.tg_id = tg_id
        super().__init__(proxy=None)

        self.__db_utils = DataBaseUtils(
            manager_config=DataBaseManagerConfig(
                action='wallets_tasks'
            )
        )

    async def _get_text(self) -> str:
        completed_tasks, uncompleted_tasks = await self.__db_utils.get_tasks_info(self.mnemonic)

        completed_tasks_list = "\n".join(f"- {task.task_name}" for task in completed_tasks) or "No tasks completed."
        uncompleted_tasks_list = "\n".join(
            f"- {task.task_name}" for task in uncompleted_tasks) or "All tasks completed."

        completed_tasks_list = escape_markdown_v2(completed_tasks_list)
        uncompleted_tasks_list = escape_markdown_v2(uncompleted_tasks_list)

        text = (
            f"💼 **Wallet completed its work:**\n"
            f"`{self.__account.wallet_address}`\n\n"
            f"📋 **Task Summary:**\n"
            f"✅ **Completed Tasks:** {len(completed_tasks)}\n"
            f"❌ **Uncompleted Tasks:** {len(uncompleted_tasks)}\n\n"
            f"🔍 **Details:**\n\n"
            f"**Completed Tasks:**\n{completed_tasks_list}\n\n"
            f"**Uncompleted Tasks:**\n{uncompleted_tasks_list}"
        )

        return text

    async def send_message(self) -> None:
        text = await self._get_text()

        await self.make_request(
            method='GET',
            url=f'https://api.telegram.org/bot{self.token}/sendMessage',
            params={
                "parse_mode": "MarkdownV2",
                "disable_web_page_preview": 1,
                "chat_id": self.tg_id,
                "text": text,
            }
        )


def escape_markdown_v2(text: str) -> str:
    specials = r"_-*[]()~`>#+=|{}.!"
    for char in specials:
        text = text.replace(char, f"\\{char}")
    return text
