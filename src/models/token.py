from __future__ import annotations
import random

from typing import Any, List, Dict
from typing_extensions import Self
from pydantic import BaseModel, Field, model_validator

from src.utils.data.tokens import TOKEN_TYPES


class Token(BaseModel):
    chain_name: str
    name: str | List[str]

    address: str | None = Field(init=False)

    @model_validator(mode='before')
    @classmethod
    def set_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        chain_name = values.get('chain_name')
        token_name = values.get('name')

        if isinstance(token_name, List):
            token_name = random.choice(token_name)
            values['name'] = token_name

        if chain_name and token_name:
            try:
                values['address'] = TOKEN_TYPES[chain_name.upper()][token_name]
            except KeyError:
                raise ValueError(f"Address for token {token_name} in chain {chain_name} not found")

        return values

    @model_validator(mode='after')
    def check_tokens_exist(self) -> Self:
        chain_name = self.chain_name
        token_name = self.name

        if isinstance(token_name, list):
            self.name = random.choice(token_name)
        else:
            self.name = token_name

        if self.name not in TOKEN_TYPES[chain_name.upper()].keys():
            raise ValueError(f'Token {self.name} does not exist in chain {chain_name}')

        return self
