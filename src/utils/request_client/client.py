from typing import Dict, Any
from loguru import logger

from aiohttp import ClientSession, TCPConnector
from aiohttp_socks import ProxyConnector

from src.utils.proxy_manager import Proxy


class RequestClient:
    def __init__(self, proxy: Proxy | None):
        self.session = ClientSession(
            connector=ProxyConnector.from_url(proxy.proxy_url, ) if proxy else TCPConnector(
                verify_ssl=False
            )
        )

    async def make_request(
            self,
            method: str = 'GET',
            url: str = None,
            headers: Dict[str, Any] = None,
            data: str = None,
            json: Dict[str, Any] = None,
            params: Dict[str, Any] = None
    ):

        async with self.session.request(
                method=method, url=url, headers=headers, data=data, params=params, json=json
        ) as response:
            try:
                if response.status in [200, 201, 202]:
                    response_json = await response.json()
                    return response_json, response.status
                else:
                    return None, response.status

            except Exception as ex:
                logger.error(f'Something went wrong {ex}')
