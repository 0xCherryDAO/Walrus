from __future__ import annotations

import random

from pydantic import BaseModel, root_validator, Field


class WithdrawSettings(BaseModel):
    token: str
    chain: str
    to_address: str
    amount: float | list[float]

    calculated_amount: float = Field(init=False)

    @root_validator(pre=True)
    def set_calculated_fields(cls, values):
        amount = values.get('amount')

        if isinstance(amount, list):
            values['calculated_amount'] = random.uniform(amount[0], amount[1])
        else:
            values['calculated_amount'] = amount

        return values


class DepositSettings(BaseModel):
    token: str
    chain: str
    to_address: str
    keep_balance: float | list[float]

    calculated_keep_balance: float = Field(init=False)

    @root_validator(pre=True)
    def set_calculated_fields(cls, values):
        keep_balance = values.get('keep_balance')

        if isinstance(keep_balance, list):
            values['calculated_keep_balance'] = random.uniform(keep_balance[0], keep_balance[1])
        else:
            values['calculated_keep_balance'] = keep_balance

        return values


class OKXConfig(BaseModel):
    deposit_settings: DepositSettings | None = None
    withdraw_settings: WithdrawSettings | None = None

    API_KEY: str
    API_SECRET: str
    PASSPHRASE: str

    PROXY: str | None


class CEXConfig(BaseModel):
    okx_config: OKXConfig | None = None
