from abc import ABC, abstractmethod
from typing import Optional

from pysui.sui.sui_txn.async_transaction import SuiTransactionAsync
from loguru import logger
from pysui import ObjectID

from config import RETRIES, PAUSE_BETWEEN_RETRIES
from src.models.swap import SwapConfig
from src.utils.common.wrappers.decorators import retry
from src.utils.data.tokens import TOKEN_TYPES
from src.utils.proxy_manager import Proxy
from src.utils.user.sui_account import SuiAccount
from src.utils.request_client.client import RequestClient


class ABCSwap(ABC, SuiAccount, RequestClient):
    def __init__(
            self,
            mnemonic: str,
            proxy: Proxy | None,
            swap_config: SwapConfig,

    ):
        self.swap_config = swap_config
        SuiAccount.__init__(
            self,
            mnemonic=mnemonic,
        )
        RequestClient.__init__(
            self, proxy=proxy
        )

    @abstractmethod
    async def create_swap_transaction(self, swap_config: SwapConfig, amount: int) -> SuiTransactionAsync:
        """Creates transaction for swap"""

    @retry(retries=RETRIES, delay=PAUSE_BETWEEN_RETRIES, backoff=1.5)
    async def swap(self) -> Optional[bool | str]:
        number_of_objects, objects = await self.get_coin_objects(
            coin_type=TOKEN_TYPES['SUI_TESTNET'][self.swap_config.from_token.name]
        )
        if number_of_objects >= 3:
            merge_to_object_id = objects[0]
            gas_object_id = objects[1]
            objects.remove(gas_object_id)
            objects.remove(merge_to_object_id)
            status, digest = await self.merge_objects(
                merge_to=ObjectID(merge_to_object_id), merge_from=objects, gas_object=ObjectID(gas_object_id)
            )
            if status is True:
                logger.success(
                    f'[{self.wallet_address}] | Successfully merged SUI tokens | '
                    f'TX: https://testnet.suivision.xyz/txblock/{digest}'
                )

        balance, coin_object_id, _ = await self.get_balance(
            coin_type=TOKEN_TYPES['SUI_TESTNET'][self.swap_config.from_token.name]
        )
        amount = int(balance * self.swap_config.swap_percentage)

        tx = await self.create_swap_transaction(self.swap_config, amount)

        status, digest = await self.send_tx(tx)

        if status is True:
            logger.success(
                f'[{self.wallet_address}] | Successfully swapped {round(amount / 10 ** 9, 4)} '
                f'{self.swap_config.from_token.name} => {self.swap_config.to_token.name} | '
                f'TX: https://testnet.suivision.xyz/txblock/{digest}'
            )
            return True
        else:
            logger.error(
                f'[{self.wallet_address}] | Transaction failed | '
                f'TX: https://testnet.suivision.xyz/txblock/{digest}'
            )
            raise Exception(f'[{self.wallet_address}] | Swap failed')
