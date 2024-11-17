from pysui.sui.sui_txn.async_transaction import SuiTransactionAsync
from pysui.sui.sui_types.bcs import Argument
from pysui.sui.sui_types import SuiString
from pysui import ObjectID, SuiAddress
from loguru import logger

from config import SUI_MAINNET_RPC, BLOCK_VISION_API_KEY, RETRIES, PAUSE_BETWEEN_RETRIES
from src.utils.common.wrappers.decorators import retry
from src.utils.proxy_manager import Proxy
from src.utils.request_client.client import RequestClient
from src.utils.user.sui_account import SuiAccount


class TradePort(SuiAccount, RequestClient):
    def __init__(
            self,
            mnemonic: str,
            proxy: Proxy | None
    ):
        SuiAccount.__init__(self, mnemonic, rpc=SUI_MAINNET_RPC)
        RequestClient.__init__(self, proxy=proxy)

    async def parse_collection(self):
        headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            'origin': 'https://www.tradeport.xyz',
            'priority': 'u=1, i',
            'referer': 'https://www.tradeport.xyz/',
            'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'x-api-key': 'vmqVu5k.fe00f6e3103ba51d835b2382e6809a2a',
            'x-api-user': 'tradeport.xyz',
        }

        json_data = {
            'query': 'query cached_fetchCollectionItems_sui_cf80d3cf_7e43_4d28_b72f_ee5bb6f5fcdb_default_1_0_50($where: listings_bool_exp!, $order_by: [listings_order_by!], $offset: Int, $limit: Int!) {\nsui {\nlistings(where: $where, order_by: $order_by, offset: $offset, limit: $limit) {\n      id\n      price\n      price_str\n      block_time\n      seller\n      market_name\n      nonce\n      coin\n      contract {\n        key\n      }\n      nft {\n        id\n        token_id\n        token_id_index\n        name\n        media_url\n        media_type\n        ranking\n        owner\n        chain_state\n        lastSale: actions(where: {type: {_in: ["buy", "accept-collection-bid", "accept-bid"]}}, order_by: {block_time: desc}, limit: 1) {\n          price\n          price_coin\n        }\n        contract {\n          commission: default_commission {\n            key\n            market_fee\n            market_name\n            royalty\n            is_custodial\n          }\n        }\n      }\n    }\n}\n}',
            'variables': {
                'limit': 50,
                'where': {
                    'collection_id': {
                        '_eq': 'cf80d3cf-7e43-4d28-b72f-ee5bb6f5fcdb',
                    },
                    'listed': {
                        '_eq': True,
                    },
                    'id': {
                        '_nin': [
                            '2028dfcd-b4c1-48f8-b89f-16d9bf1e831f',
                            '02016d95-6bff-44c5-9e0d-60060c2db0c3',
                            'd9c99fdb-b354-4c93-99c0-c5f19be6c125',
                            'e1ff3e51-62ef-476a-bc62-16decdc3966c',
                            '07954f15-5489-4631-8459-63824e979ad5',
                            '3d093e81-aef7-4ee6-b178-310cd5a24265',
                            '7c670ec5-0f69-4de7-b41f-d272423f0b32',
                            '29d3edc5-4de1-47e9-8875-c855ee8f3e53',
                            'f7fcf3a0-5f9b-4fd4-a568-f707f30c6101',
                            'd8b4ce0d-e05e-4f9b-bfc9-4ff9876c3659',
                            'ed71fdef-8733-48c8-95ca-fe19234186ac',
                            '59a87630-6e66-456c-b921-ee84c4b18c55',
                            '56922829-c725-4728-8fed-355b525c7341',
                            'b1074570-58e0-43e6-a20b-0805c0cfb852',
                            'ad139730-c6d0-4d26-ab40-be80f4f8960d',
                            '473e35ab-426a-43de-888a-06382e373a2b',
                            '753c08ad-51a6-4f31-8dd4-5009fa53a0d1',
                            '851f8153-7660-4d90-947e-62ce090813b0',
                            '7e1911ab-009c-4001-a89a-13cd2bdf401c',
                            'bd8b8dc1-58f2-418a-ad7c-1305d31913b2',
                            '9e4cf931-6c77-4892-9f4d-0e788c47378a',
                            '9271f2d8-5afc-4c13-9bcd-10bfeb8ddf5e',
                            '7ae7b34f-e657-470f-b778-404e09227838',
                            '20d8a5e4-b50e-4aea-a4d1-ffde9f83bc7c',
                            '6b81e67c-cf64-4f89-b75f-60f12067ede3',
                            'ad004228-683f-4f73-ad61-9e739e684da9',
                            '3fd59aea-85a9-4ca6-972f-a622e5cd5ede',
                            '2107dfe9-0176-430c-a4b4-65e11cd0fb4f',
                            '69214fb5-31a8-4b9e-86b1-217365bb7c8c',
                            '80f3928e-d405-4972-836c-a94872ec66be',
                            'd7955aeb-9ea7-4dfa-bb09-c3c889e2220f',
                            'e8b3f005-06db-432f-a955-e23796a6c2b6',
                            'cb77de8c-d8d8-4248-9fa2-07f2bb77b1af',
                            '648051d9-f738-45a6-b7e2-a5b432c35ab5',
                            '0adf56d2-8ae1-406e-a0d3-3ebe47e9f0e2',
                            '4553f7db-3d25-415f-985b-248b5b709396',
                            'ea642630-8813-4e72-8e84-4b7fcbd269e9',
                            '4c665acc-4990-416c-8f56-161cf6f9450f',
                            '58dbf633-b046-4f78-b8fa-14ea5fa4e2cc',
                            '9d2398f2-77dd-4f4c-80fa-f96a3209f1a3',
                            'f7fc5ab0-7f81-42f4-a76c-90ef13cb131e',
                            '9b3a2303-6f18-456f-b97e-d0323fc0f66a',
                        ],
                    },
                    'market_name': {
                        '_neq': 'marketplace',
                    },
                },
                'order_by': {
                    'price': 'asc_nulls_last',
                },
                'offset': 0,
            },
            'operationName': 'cached_fetchCollectionItems_sui_cf80d3cf_7e43_4d28_b72f_ee5bb6f5fcdb_default_1_0_50',
        }
        response_json, _ = await self.make_request(
            method="POST",
            url='https://api.indexer.xyz/graphql',
            headers=headers,
            json=json_data
        )
        best_listing = response_json['data']['sui']['listings'][0]
        price = best_listing['price']
        nonce = best_listing['nonce']
        return price, nonce

    def __str__(self) -> str:
        return f'[{self.wallet_address}] | [{self.__class__.__name__}] | [Buying Walrus NFT...]'

    @retry(retries=RETRIES, delay=PAUSE_BETWEEN_RETRIES, backoff=1.5)
    async def buy_nft(self) -> bool:
        if BLOCK_VISION_API_KEY:
            already_have = await self.check_if_already_have_nft()
            if already_have:
                return True

        price, nonce = await self.parse_collection()

        tx = SuiTransactionAsync(client=self.client)

        object_data = await self.client.get_object(
            ObjectID(
                '0x47cba0b6309a12ce39f9306e28b899ed4b3698bce4f4911fd0c58ff2329a2ff6'
            )
        )
        object_data = object_data.result_data

        await tx.split_coin(
            coin=Argument('GasCoin'),
            amounts=[price]
        )

        await tx.move_call(
            target=SuiString(f"0xb42dbb7413b79394e1a0175af6ae22b69a5c7cc5df259cd78072b6818217c027::listings::buy"),
            type_arguments=['0x5d9865999eb9a4a5d7cb6615260e42c6400aec1b34cfbb2070005925e673e92e::deliver::GalxeNFT'],
            arguments=[
                object_data,
                SuiAddress(nonce),
                Argument('NestedResult', (0, 0))
            ]
        )
        await tx.move_call(
            target=SuiString(
                '0x0000000000000000000000000000000000000000000000000000000000000002::coin::destroy_zero'),
            type_arguments=['0x2::sui::SUI'],
            arguments=[Argument('NestedResult', (0, 0))]
        )

        status, digest = await self.send_tx(tx)

        if status is True:
            logger.success(
                f'[{self.wallet_address}] | Successfully bought Walrus NFT for {price / 10 ** 9} SUI | '
                f'TX: https://suivision.xyz/txblock/{digest}'
            )
            return True
        else:
            logger.error(f'[{self.wallet_address}] | Transaction failed | TX: https://suivision.xyz/txblock/{digest}')
            raise Exception(f'[{self.wallet_address}] | Buy failed')

    async def check_if_already_have_nft(self) -> bool:
        headers = {
            'accept': 'application/json',
            'x-api-key': BLOCK_VISION_API_KEY,
        }
        page = 1
        while True:
            params = {
                'account': str(self.wallet_address),
                'type': 'non-kiosk',
                'pageIndex': str(page),
                'pageSize': '50',
            }
            response_json = await self.make_request(
                url='https://api.blockvision.org/v2/sui/account/nfts',
                params=params,
                headers=headers
            )
            page += 1
            data = response_json[0]['result']['data']
            if not data:
                logger.warning(f"[{self.wallet_address}] | This wallet doesn't have nft")
                break

            for nft in data:
                name = nft['name']
                if name == 'Walrus Explorer':
                    logger.success(f"[{self.wallet_address}] | This wallet already has nft")
                    return True
