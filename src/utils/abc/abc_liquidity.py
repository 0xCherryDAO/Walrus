from abc import ABC, abstractmethod
from typing import Optional

from pysui.sui.sui_txn.async_transaction import SuiTransactionAsync
from pysui import ObjectID
from loguru import logger

from config import RETRIES, PAUSE_BETWEEN_RETRIES
from src.models.liquidity import LiquidityConfig
from src.utils.common.wrappers.decorators import retry
from src.utils.data.tokens import TOKEN_TYPES
from src.utils.proxy_manager import Proxy
from src.utils.user.sui_account import SuiAccount
from src.utils.request_client.client import RequestClient


class ABCLiquidity(ABC, SuiAccount, RequestClient):
    def __init__(
            self,
            mnemonic: str,
            proxy: Proxy | None,
            liquidity_config: LiquidityConfig,
    ):
        self.liquidity_config = liquidity_config
        SuiAccount.__init__(
            self,
            mnemonic=mnemonic,
        )
        RequestClient.__init__(
            self, proxy=proxy
        )

    @abstractmethod
    async def create_staking_transaction(
            self, liquidity_config: LiquidityConfig, amount: int, object_id: ObjectID
    ) -> SuiTransactionAsync:
        """Creates transaction for swap"""

    @retry(retries=RETRIES, delay=PAUSE_BETWEEN_RETRIES, backoff=1.5)
    async def add_liquidity(self) -> Optional[bool]:
        number_of_objects, objects = await self.get_coin_objects(
            coin_type=TOKEN_TYPES['SUI_TESTNET'][self.liquidity_config.token.name]
        )
        if number_of_objects >= 3:
            merge_to_object_id = objects[0]
            if self.liquidity_config.token == 'SUI':
                gas_object_id = objects[1]
                objects.remove(gas_object_id)
            else:
                gas_object_id = await self.get_gas_object()

            objects.remove(merge_to_object_id)
            status, digest = await self.merge_objects(
                merge_to=ObjectID(merge_to_object_id), merge_from=objects, gas_object=ObjectID(gas_object_id)
            )
            if status is True:
                logger.success(
                    f'[{self.wallet_address}] | Successfully merged {self.liquidity_config.token.name} tokens | '
                    f'TX: https://testnet.suivision.xyz/txblock/{digest}'
                )

        balance, coin_object_id, _ = await self.get_balance(
            coin_type=TOKEN_TYPES['SUI_TESTNET'][self.liquidity_config.token.name]
        )
        amount = int(balance * self.liquidity_config.stake_percentage)
        if self.liquidity_config.stake_all_balance:
            amount = balance

        tx = await self.create_staking_transaction(self.liquidity_config, amount, ObjectID(coin_object_id))

        status, digest = await self.send_tx(tx)

        if status is True:
            logger.success(
                f'[{self.wallet_address}] | Successfully staked {round(amount / 10 ** 9, 4)} WAL...'
                f'TX: https://testnet.suivision.xyz/txblock/{digest}'
            )
            return True
        else:
            logger.error(
                f'[{self.wallet_address}] | Transaction failed | '
                f'TX: https://testnet.suivision.xyz/txblock/{digest}'
            )
            raise Exception(f'[{self.wallet_address}] | Stake failed')
