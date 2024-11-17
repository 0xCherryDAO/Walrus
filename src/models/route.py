from __future__ import annotations

from typing import List, Any

from pydantic import BaseModel, model_validator, Field

from config import MOBILE_PROXY
from src.utils.proxy_manager import Proxy


class Wallet(BaseModel):
    mnemonic: str
    recipient: str | None = None
    proxy: Any | None = Field(init=False)

    @model_validator(mode='before')
    def set_proxy(cls, values):
        proxy = values.get('proxy')

        change_link = None
        if proxy:
            if MOBILE_PROXY:
                proxy_url, change_link = proxy.split('|')
            else:
                proxy_url = proxy

            proxy = Proxy(proxy_url=f'http://{proxy_url}', change_link=change_link)
            values['proxy'] = proxy

        return values


class Route(BaseModel):
    tasks: List[str]
    wallet: Wallet
