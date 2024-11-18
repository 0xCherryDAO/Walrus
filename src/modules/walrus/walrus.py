import random

from pysui import ObjectID, SuiAddress
from pysui.sui.sui_txn.async_transaction import SuiTransactionAsync
from pysui.sui.sui_types import SuiString
from pysui.sui.sui_types.bcs import Argument

from src.models.liquidity import LiquidityConfig
from src.models.swap import SwapConfig
from src.utils.abc.abc_liquidity import ABCLiquidity
from src.utils.abc.abc_swap import ABCSwap
from src.utils.data.tokens import WALRUS_POOLS
from src.utils.proxy_manager import Proxy


class Walrus(ABCSwap, ABCLiquidity):
    def __init__(
            self,
            mnemonic: str,
            proxy: Proxy | None,
            swap_config: SwapConfig = None,
            liquidity_config: LiquidityConfig = None
    ):
        ABCSwap.__init__(
            self,
            mnemonic=mnemonic,
            proxy=proxy,
            swap_config=swap_config,
        )
        ABCLiquidity.__init__(
            self,
            mnemonic=mnemonic,
            proxy=proxy,
            liquidity_config=liquidity_config
        )

    def __str__(self) -> str:
        if self.swap_config:
            return f'[{self.wallet_address}] | Swapping {round(self.swap_config.swap_percentage * 100, 3)}% SUI => WAL'
        elif self.liquidity_config:
            return f'[{self.wallet_address}] | Staking WAL...'

    async def create_swap_transaction(self, swap_config: SwapConfig, amount: int) -> SuiTransactionAsync:
        tx = SuiTransactionAsync(client=self.client)
        await tx.split_coin(
            coin=Argument('GasCoin'),
            amounts=[amount]
        )
        move_call_result = await tx.move_call(
            target=SuiString(
                "0x9f992cc2430a1f442ca7a5ca7638169f5d5c00e0ebc3977a65e9ac6e497fe5ef::wal_exchange::exchange_all_for_wal"
            ),
            arguments=[
                ObjectID("0x0e60a946a527902c90bbc71240435728cd6dc26b9e8debc69f09b71671c3029b"),
                Argument("NestedResult", (0, 0))
            ],
        )
        await tx.transfer_objects(
            transfers=[move_call_result],
            recipient=self.config.active_address
        )
        return tx

    async def create_staking_transaction(
            self, liquidity_config: LiquidityConfig, amount: int, object_id: ObjectID
    ) -> SuiTransactionAsync:
        tx = SuiTransactionAsync(client=self.client)

        await tx.split_coin(
            coin=object_id,
            amounts=[amount]
        )
        move_call_result = await tx.move_call(
            target=SuiString(
                "0x9f992cc2430a1f442ca7a5ca7638169f5d5c00e0ebc3977a65e9ac6e497fe5ef::staking::stake_with_pool"),
            arguments=[
                ObjectID("0x37c0e4d7b36a2f64d51bba262a1791f844cfd88f31379f1b7c04244061d43914"),
                Argument("NestedResult", (0, 0)),
                SuiAddress(random.choice(WALRUS_POOLS))
            ],
        )
        await tx.transfer_objects(
            transfers=[move_call_result],
            recipient=self.config.active_address
        )
        return tx
