from __future__ import annotations

from typing import List, Any, Dict
import random

from pydantic import model_validator, BaseModel
from src.models.token import Token


class LiquidityConfig(BaseModel):
    token: Token

    amount: float | List[float]
    use_percentage: bool
    stake_percentage: float | List[float]
    stake_all_balance: bool

    @model_validator(mode='before')
    @classmethod
    def validate_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        amount = values.get('amount')
        stake_percentage = values.get('stake_percentage')

        if isinstance(amount, List):
            if len(amount) != 2 or not all(isinstance(i, (int, float)) for i in amount):
                raise ValueError('amount list must contain exactly two numeric values')
            values['amount'] = round(random.uniform(amount[0], amount[1]), 7)
        elif isinstance(amount, (int, float)):
            values['amount'] = amount

        if isinstance(stake_percentage, List):
            if len(stake_percentage) != 2 or not all(isinstance(i, (int, float)) for i in stake_percentage):
                raise ValueError('stake_percentage list must contain exactly two numeric values')
            values['stake_percentage'] = random.uniform(stake_percentage[0], stake_percentage[1])
        elif isinstance(stake_percentage, (int, float)):
            values['stake_percentage'] = stake_percentage

        return values
