MOBILE_PROXY = False
ROTATE_IP = False

RETRIES = 3
PAUSE_BETWEEN_RETRIES = 10

SUI_TESTNET_RPC = 'https://fullnode.testnet.sui.io:443'
SUI_MAINNET_RPC = 'https://fullnode.mainnet.sui.io:443'

BLOCK_VISION_API_KEY = None  # API_KEY (str) | None (https://dashboard.blockvision.org/overview)

TG_BOT_TOKEN = None  # str
TG_USER_ID = None  # int

SHUFFLE_WALLETS = False
PAUSE_BETWEEN_WALLETS = [1, 2]
PAUSE_BETWEEN_MODULES = [1, 2]

# --- CEXs --- #
WITHDRAW_FROM_OKX = False  # From OKX to Wallets

# --- Testnet --- #
FAUCET = False
SWAP = False  # Swap SUI => WAL
STAKE = False  # WAL Staking
MINT_FLATLAND_NFT = False

# --- Mainnet --- #
BUY_WALRUS_NFT = False  # Walrus Explorer NFT | MAINNET


# --- Testnet activities ---#
class SwapSettings:
    swap_percentage = [0.8, 0.9]


class LiquiditySettings:
    use_percentage = False
    stake_percentage = [0.4, 0.5]
    stake_all_balance = True


# --- CEXs --- #
class OKXWithdrawSettings:  # From OKX to Wallets
    chain = 'SUI'
    token = 'SUI'
    amount = [0.1, 0.15]  # (0.06 SUI fee | 0.1 min)

    min_sui_balance = 0.1  # Minimum balance above which there will be no withdrawal


class OKXSettings:
    API_KEY = ''
    API_SECRET = ''
    API_PASSWORD = ''

    PROXY = None  # 'http://login:pass@ip:port'
