from abc import ABC, abstractmethod
from asyncio import sleep
from typing import Callable, Optional

import ccxt
from loguru import logger

from config import SUI_MAINNET_RPC, OKXWithdrawSettings

from src.models.cex import CEXConfig
from src.utils.proxy_manager import Proxy
from src.utils.request_client.client import RequestClient
from src.utils.user.sui_account import SuiAccount


class CEX(ABC, SuiAccount, RequestClient):
    def __init__(
            self,
            mnemonic: str,
            proxy: Proxy | None,
            config: CEXConfig
    ):
        self.amount = None
        self.token = None
        self.chain: Optional[str] = None
        self.to_address = None
        self.keep_balance = None
        self.api_key = None
        self.api_secret = None
        self.passphrase = None
        self.password = None
        self.proxy = None
        self.exchange_instance = None

        self.cex_config = config
        if config.okx_config:
            self.setup_exchange(exchange_config=config.okx_config, exchange_type='okx')
        elif config.binance_config:
            self.setup_exchange(exchange_config=config.binance_config, exchange_type='binance')
        elif config.bitget_config:
            self.setup_exchange(exchange_config=config.bitget_config, exchange_type='bitget')

        # rpc = chain_mapping[self.chain.upper()].rpc
        SuiAccount.__init__(
            self, mnemonic, rpc=SUI_MAINNET_RPC
        )
        RequestClient.__init__(
            self, proxy=self.proxy
        )

    @abstractmethod
    def call_withdraw(self, exchange_instance) -> Optional[bool]:
        """Calls withdraw function"""

    @abstractmethod
    async def call_sub_transfer(
            self, token: str, api_key: str, api_secret: str, api_passphrase: Optional[str],
            api_password: Optional[str], request_func: Callable
    ):
        """Calls transfer from sub-account to main-account"""

    async def withdraw(self) -> Optional[bool]:
        balance_before_withdraw, _, objects_before = await self.get_balance(coin_type='0x2::sui::SUI')

        min_sui_balance = OKXWithdrawSettings.min_sui_balance
        if balance_before_withdraw >= min_sui_balance:
            logger.success(f'[{self.wallet_address}] | Balance is already greater than {min_sui_balance}')
            return True
        logger.debug(f'Checking sub-accounts balances before withdrawal...')
        await self.call_sub_transfer(
            self.token, self.api_key, self.api_secret, self.passphrase, self.password, self.make_request
        )
        await sleep(10)
        withdrawn = self.call_withdraw(self.exchange_instance)
        if withdrawn:
            await self.wait_for_withdrawal(balance_before_withdraw, objects_before)
            return True

    # async def deposit(self) -> Optional[bool]:
    #     pass

    async def wait_for_withdrawal(
            self, balance_before_withdraw: int, objects_before: int | None = None
    ) -> None:
        logger.info(f'Waiting for {self.token} to arrive...')
        while True:
            try:
                current_balance, _, current_objects = await self.get_balance(coin_type='0x2::sui::SUI')
                if current_objects > objects_before:
                    logger.success(f'[{self.wallet_address}] | SUI has arrived.')
                    break
                await sleep(10)
            except Exception as ex:
                logger.error(ex)
                await sleep(5)
                continue

    def setup_exchange(self, exchange_config, exchange_type):
        if exchange_config.withdraw_settings:
            self.amount = exchange_config.withdraw_settings.calculated_amount
            self.token = exchange_config.withdraw_settings.token
            self.chain = exchange_config.withdraw_settings.chain
            self.to_address = exchange_config.withdraw_settings.to_address

        self.api_key = exchange_config.API_KEY
        self.api_secret = exchange_config.API_SECRET
        self.proxy = exchange_config.PROXY

        if exchange_type == 'okx':
            self.passphrase = exchange_config.PASSPHRASE
            self.exchange_instance = ccxt.okx({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'password': self.passphrase,
                'enableRateLimit': True,
                'proxies': self.get_proxies(self.proxy)
            })
        elif exchange_type == 'binance':
            self.exchange_instance = ccxt.binance({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'enableRateLimit': True,
                'proxies': self.get_proxies(self.proxy),
                'options': {'defaultType': 'spot'}
            })
        elif exchange_type == 'bitget':
            self.password = exchange_config.PASSWORD
            self.exchange_instance = ccxt.bitget({
                'apiKey': self.api_key,
                'secret': self.api_secret,
                'password': self.password,
                'enableRateLimit': True,
                'proxies': self.get_proxies(self.proxy),
                'options': {'defaultType': 'spot'}
            })

        if exchange_config.deposit_settings:
            self.token = exchange_config.deposit_settings.token
            self.chain = exchange_config.deposit_settings.chain
            self.to_address = exchange_config.deposit_settings.to_address
            self.keep_balance = exchange_config.deposit_settings.calculated_keep_balance

    @staticmethod
    def get_proxies(proxy: str | None) -> dict[str, str | None]:
        return {
            'http': proxy if proxy else None,
            'https': proxy if proxy else None
        }
