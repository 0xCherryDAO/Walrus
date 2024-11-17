from typing import Optional, Callable

from loguru import logger

from src.modules.cex.okx.utils.okx_sub_transfer import transfer_from_subaccs_to_main
from src.models.cex import CEXConfig
from src.modules.cex.okx.utils.data import get_withdrawal_fee
from src.utils.proxy_manager import Proxy
from src.utils.abc.abc_cex import CEX


class OKX(CEX):
    def __init__(
            self,
            config: CEXConfig,
            mnemonic: str,
            proxy: Proxy | None
    ):
        super().__init__(mnemonic=mnemonic, proxy=proxy, config=config)

    def __str__(self) -> str:
        if self.cex_config.okx_config.withdraw_settings:
            return (
                f'[{self.wallet_address}] | [{self.__class__.__name__}] | '
                f'Withdrawing {round(self.amount, 5)} {self.token} '
                f'to {self.to_address} | CHAIN: {self.chain}')
        else:
            return (f'[{self.wallet_address}] | [{self.__class__.__name__}] | Depositing {self.token}'
                    f' to {self.to_address} | CHAIN: {self.chain}')

    def call_withdraw(self, exchange_instance) -> Optional[bool]:
        try:
            chain_name = self.token + '-' + self.chain
            fee = get_withdrawal_fee(self.token, chain_name, exchange_instance)
            self.exchange_instance.withdraw(
                self.token.upper(),
                self.amount,
                self.to_address,
                params={
                    'toAddress': self.to_address,
                    'chainName': chain_name,
                    'dest': 4,
                    'fee': fee,
                    'pwd': '-',
                    'amt': self.amount,
                    'network': self.chain
                }
            )

            logger.success(
                f'Successfully withdrawn {self.amount} {self.token} to {self.chain} for wallet {self.to_address}'
            )
            return True

        except Exception as ex:
            logger.error(f'Something went wrong {ex}')
            return

    async def call_sub_transfer(
            self, token: str, api_key: str, api_secret: str, api_passphrase: Optional[str],
            api_password: Optional[str], request_func: Callable
    ):
        await transfer_from_subaccs_to_main(
            token=token, make_request=request_func
        )
