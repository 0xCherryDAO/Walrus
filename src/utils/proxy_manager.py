from aiohttp import ClientSession
from asyncio import sleep

from loguru import logger


class Proxy:
    def __init__(
            self,
            proxy_url: str,
            change_link: str
    ):
        self.proxy_url = proxy_url
        self.change_link = change_link

    async def change_ip(self) -> None:
        while True:
            try:
                async with ClientSession() as session:
                    response = await session.get(self.change_link)
                    if response.status != 200:
                        logger.error(f'Failed to change ip')
                        continue
                    # logger.success('Successfully changed ip')
                    break

            except Exception as ex:
                logger.error(ex)
                await sleep(4)
                continue
