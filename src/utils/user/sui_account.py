from typing import Optional, Union

from pysui.abstracts import SignatureScheme
from pysui import SuiConfig, AsyncClient, SuiAddress, ObjectID
from pysui.sui.sui_txn.async_transaction import SuiTransactionAsync
from pysui.sui.sui_types import SuiTxBytes, SuiString

from config import SUI_TESTNET_RPC
from src.utils.data.tokens import TOKEN_TYPES


class SuiAccount:
    def __init__(
            self,
            mnemonic: str,
            rpc: str = SUI_TESTNET_RPC
    ):
        if mnemonic.startswith('0x'):
            key_format = {
                'wallet_key': mnemonic,
                'key_scheme': SignatureScheme.ED25519
            }
            self.config = SuiConfig.user_config(
                rpc_url=rpc,
                prv_keys=[key_format]
            )
        elif mnemonic.startswith('suiprivkey'):
            self.config = SuiConfig.user_config(
                rpc_url=rpc,
                prv_keys=[mnemonic]
            )
        else:
            self.config = SuiConfig.user_config(rpc_url=rpc)
            self.config.recover_keypair_and_address(
                scheme=SignatureScheme.ED25519,
                mnemonics=mnemonic,
                derivation_path="m/44'/784'/0'/0'/0'"
            )
        self.config.set_active_address(address=SuiAddress(self.config.addresses[0]))

        self.client = AsyncClient(self.config)
        self.wallet_address = self.client.config.active_address

    async def send_tx(self, tx: SuiTransactionAsync) -> tuple[bool, str]:
        tx_bytes = await tx.deferred_execution()
        sui_tx_bytes = SuiTxBytes(tx_bytes)
        sign_and_submit_res = await self.client.sign_and_submit(
            signer=self.config.active_address,
            tx_bytes=sui_tx_bytes
        )

        result_data = sign_and_submit_res.result_data
        status = True if result_data.effects.status.status == 'success' else False
        digest = result_data.digest
        return status, digest

    async def execute_tx(self, tx: SuiTransactionAsync, gas_object: Union[ObjectID, str]):
        execute_res = await tx.execute(
            use_gas_object=gas_object,
            run_verification=True
        )
        result_data = execute_res.result_data
        status = True if result_data.effects.status.status == 'success' else False
        digest = result_data.digest
        return status, digest

    async def get_balance(self, coin_type: Union[SuiString, str]) -> tuple[int, str | None, Optional[int]]:
        token = (
            await self.client.get_coin(
                coin_type=coin_type, address=self.config.active_address
            )
        ).result_data.to_dict()['data']
        if not token:
            return 0, None, 0
        balance = int(token[0]['balance'])
        coin_object_id = token[0]['coinObjectId']
        return balance, coin_object_id, len(token)

    async def merge_objects(
            self,
            merge_to: Union[ObjectID, str],
            merge_from: list[Union[ObjectID, str]],
            gas_object: Union[ObjectID, str]
    ) -> tuple[bool, str]:
        tx = SuiTransactionAsync(client=self.client)
        await tx.merge_coins(
            merge_to=merge_to,
            merge_from=merge_from,
        )
        status, digest = await self.execute_tx(tx, gas_object)
        return status, digest

    async def get_coin_objects(self, coin_type: Union[SuiString, str]) -> tuple[int, Optional[list[str]]]:
        token_objects = (
            await self.client.get_coin(
                coin_type=coin_type, address=self.config.active_address
            )
        ).result_data.to_dict()['data']
        if not token_objects:
            return 0, None

        objects = [token['coinObjectId'] for token in token_objects]
        number_of_objects = len(objects)
        return number_of_objects, objects

    async def get_gas_object(self) -> ObjectID:
        _, coin_object_id, _ = await self.get_balance(
            coin_type=TOKEN_TYPES['SUI_TESTNET']['SUI']
        )
        return ObjectID(coin_object_id)
