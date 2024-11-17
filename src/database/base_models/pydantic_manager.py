from pydantic import BaseModel, validator, Field, root_validator

from src.database.models import (
    WorkingWallets,
    WalletsTasks,
)


class DataBaseManagerConfig(BaseModel):
    action: str

    calculated_table_object: object = Field(init=False)

    @validator('action', pre=True)
    def validate_action(cls, v):
        if v not in ['working_wallets', 'wallets_tasks']:
            raise ValueError(f'...')
        return v

    @root_validator(pre=True)
    def set_calculated_fields(cls, values):
        table_mapping = {
            'working_wallets': WorkingWallets,
            'wallets_tasks': WalletsTasks,

        }
        action = values.get('action')

        values['calculated_table_object'] = table_mapping[action]

        return values
