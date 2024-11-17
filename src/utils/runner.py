from typing import Optional

from loguru import logger

from config import *
from src.models.liquidity import LiquidityConfig
from src.models.swap import SwapConfig
from src.models.token import Token
from src.modules.faucet.testnet_faucet import SuiTestnetFaucet
from src.models.route import Route
from src.modules.nft.flatland.flatland_nft import FlatLand
from src.modules.nft.tradeport.walrus_nft import TradePort
from src.modules.walrus.walrus import Walrus

from src.models.cex import WithdrawSettings as WithdrawCexSettings
from src.modules.cex.okx.okx import OKX
from src.models.cex import CEXConfig, OKXConfig
from src.utils.user.sui_account import SuiAccount


async def process_faucet(mnemonic: str, route: Route) -> Optional[bool]:
    faucet = SuiTestnetFaucet(
        mnemonic=mnemonic,
        proxy=route.wallet.proxy,
    )
    logger.debug(faucet)
    requested = await faucet.request_tokens()
    if requested:
        return True


async def process_swap(mnemonic: str, route: Route) -> Optional[bool]:
    swap_config = SwapConfig(
        from_token=Token(
            chain_name='SUI_TESTNET',
            name='SUI'
        ),
        to_token=Token(
            chain_name='SUI_TESTNET',
            name='WAL'
        ),
        amount=0,
        use_percentage=True,
        swap_percentage=SwapSettings.swap_percentage,
        swap_all_balance=False,
    )

    walrus = Walrus(
        mnemonic=mnemonic,
        proxy=route.wallet.proxy,
        swap_config=swap_config
    )
    logger.debug(walrus)
    swapped = await walrus.swap()
    if swapped:
        return True


async def process_staking(mnemonic: str, route: Route) -> Optional[bool]:
    liquidity_config = LiquidityConfig(
        token=Token(
            chain_name='SUI_TESTNET',
            name='WAL',
        ),
        amount=0,
        use_percentage=LiquiditySettings.use_percentage,
        stake_percentage=LiquiditySettings.stake_percentage,
        stake_all_balance=LiquiditySettings.stake_all_balance
    )

    walrus = Walrus(
        mnemonic=mnemonic,
        proxy=route.wallet.proxy,
        liquidity_config=liquidity_config
    )
    logger.debug(walrus)
    staked = await walrus.add_liquidity()
    if staked:
        return True


async def process_buy_on_trade_port(mnemonic: str, route: Route) -> bool:
    trade_port = TradePort(
        mnemonic=mnemonic,
        proxy=route.wallet.proxy,
    )
    bought = await trade_port.buy_nft()
    if bought:
        return True


async def process_mint_flatland(mnemonic: str, route: Route) -> bool:
    flatland = FlatLand(
        mnemonic=mnemonic,
        proxy=route.wallet.proxy,
    )
    bought = await flatland.mint_nft()
    if bought:
        return True


async def process_cex_withdraw(mnemonic: str, proxy: str | None) -> bool:
    account = SuiAccount(mnemonic, rpc=SUI_MAINNET_RPC)

    chain = OKXWithdrawSettings.chain
    token = OKXWithdrawSettings.token
    amount = OKXWithdrawSettings.amount

    okx_config = OKXConfig(
        deposit_settings=None,
        withdraw_settings=WithdrawCexSettings(
            token=token,
            chain=chain,
            to_address=str(account.wallet_address),
            amount=amount
        ),
        API_KEY=OKXSettings.API_KEY,
        API_SECRET=OKXSettings.API_SECRET,
        PASSPHRASE=OKXSettings.API_PASSWORD,
        PROXY=OKXSettings.PROXY
    )

    config = CEXConfig(
        okx_config=okx_config,
    )
    cex = OKX(
        config=config,
        mnemonic=mnemonic,
        proxy=proxy
    )

    logger.debug(cex)
    withdrawn = await cex.withdraw()

    if withdrawn is True:
        return True
