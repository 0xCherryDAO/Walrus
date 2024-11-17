from pysui.sui.sui_txn.async_transaction import SuiTransactionAsync
from pysui.sui.sui_types import SuiString
from pysui import ObjectID, SuiAddress
from loguru import logger

from config import RETRIES, PAUSE_BETWEEN_RETRIES
from src.utils.common.wrappers.decorators import retry
from src.utils.proxy_manager import Proxy
from src.utils.request_client.client import RequestClient
from src.utils.user.sui_account import SuiAccount


class FlatLand(SuiAccount, RequestClient):
    def __init__(
            self,
            mnemonic: str,
            proxy: Proxy | None
    ):
        SuiAccount.__init__(self, mnemonic)
        RequestClient.__init__(self, proxy=proxy)

    def __str__(self) -> str:
        return f'[{self.wallet_address}] | [{self.__class__.__name__}] | [Minting FlatLand NFT...]'

    @retry(retries=RETRIES, delay=PAUSE_BETWEEN_RETRIES, backoff=1.5)
    async def mint_nft(self) -> bool:
        tx = SuiTransactionAsync(client=self.client)

        await tx.move_call(
            target=SuiString("0x4cb65566af16acb9ae48c437e99653e77c06c1b712329486987223ca99f44575::flatland::mint"),
            arguments=[
                ObjectID("0x0000000000000000000000000000000000000000000000000000000000000008")
            ]
        )

        status, digest = await self.send_tx(tx)

        if status is True:
            logger.success(
                f'[{self.wallet_address}] | Successfully minted FlatLand NFT | '
                f'TX: https://testnet.suivision.xyz/txblock/{digest}'
            )
            return True
        else:
            logger.error(
                f'[{self.wallet_address}] | Transaction failed '
                f'| TX: https://testnet.suivision.xyz/txblock/{digest}'
            )
            raise Exception(f'[{self.wallet_address}] | Mint failed')
