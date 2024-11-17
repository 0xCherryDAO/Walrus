from asyncio import sleep, wait_for
from typing import Optional

import pyuseragents
from loguru import logger

from src.utils.proxy_manager import Proxy
from src.utils.request_client.client import RequestClient
from src.utils.user.sui_account import SuiAccount


class SuiTestnetFaucet(SuiAccount, RequestClient):
    def __init__(
            self,
            mnemonic: str,
            proxy: Proxy | None
    ):
        SuiAccount.__init__(self, mnemonic=mnemonic)
        RequestClient.__init__(self, proxy=proxy)

    def __str__(self) -> str:
        return f'[{self.wallet_address}] | Requesting tokens...'

    async def request_tokens(self) -> Optional[bool]:
        faucet_headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://faucet.blockbolt.io',
            'priority': 'u=1, i',
            'referer': 'https://faucet.blockbolt.io/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': pyuseragents.random(),
        }
        json_data = {
            'FixedAmountRequest': {
                'recipient': str(self.wallet_address),
            },
        }
        testnet_balance_before, _, objects_before = await self.get_balance(coin_type='0x2::sui::SUI')

        response_json, status = await self.make_request(
            method='POST',
            url='https://faucet.testnet.sui.io/v1/gas',
            headers=faucet_headers,
            json=json_data
        )
        if status == 202:
            logger.success(f'[{self.wallet_address}] | Successfully requested tokens')
            try:
                arrived = await wait_for(
                    fut=self.wait_for_arrive(objects_before=objects_before),
                    timeout=400
                )
                if arrived:
                    return True
            except TimeoutError:
                return False
        else:
            logger.error(f'[{self.wallet_address}] | Request failed | STATUS CODE: {status}')

    async def wait_for_arrive(self, objects_before: int) -> bool:
        logger.debug(f'[{self.wallet_address}] | Waiting for SUI to arrive')
        while True:
            try:
                current_balance, _, current_objects = await self.get_balance(coin_type='0x2::sui::SUI')
                if current_objects > objects_before:
                    logger.success(f'[{self.wallet_address}] | SUI has arrived.')
                    return True
                await sleep(10)
            except Exception as ex:
                logger.error(ex)
                await sleep(5)
