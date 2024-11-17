from src.utils.runner import *

module_handlers = {
    'FAUCET': process_faucet,
    'SWAP': process_swap,
    'STAKE': process_staking,
    'BUY_NFT': process_buy_on_trade_port,
    'WITHDRAW_FROM_OKX': process_cex_withdraw,
    'MINT_FLATLAND_NFT': process_mint_flatland
}
