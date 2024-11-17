from __future__ import annotations

from typing import List, Any, Dict
import random

from pydantic import model_validator, BaseModel
from src.models.token import Token


class SwapConfig(BaseModel):
    from_token: Token
    to_token: Token

    amount: float | List[float]
    use_percentage: bool
    swap_percentage: float | List[float]
    swap_all_balance: bool

    @model_validator(mode='before')
    @classmethod
    def validate_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        amount = values.get('amount')
        swap_percentage = values.get('swap_percentage')

        if isinstance(amount, List):
            if len(amount) != 2 or not all(isinstance(i, (int, float)) for i in amount):
                raise ValueError('amount list must contain exactly two numeric values')
            values['amount'] = round(random.uniform(amount[0], amount[1]), 7)
        elif isinstance(amount, (int, float)):
            values['amount'] = amount

        if isinstance(swap_percentage, List):
            if len(swap_percentage) != 2 or not all(isinstance(i, (int, float)) for i in swap_percentage):
                raise ValueError('swap_percentage list must contain exactly two numeric values')
            values['swap_percentage'] = random.uniform(swap_percentage[0], swap_percentage[1])
        elif isinstance(swap_percentage, (int, float)):
            values['swap_percentage'] = swap_percentage

        return values
