from datetime import datetime

from pydantic import BaseModel, Field, field_validator
from decimal import Decimal

from app.enum import CurrencyEnum


class OperationRequest(BaseModel):
    wallet_name: str = Field(..., max_length=128)
    amount: Decimal
    description: str | None = Field(None, max_length=250)

    @field_validator('amount')
    def amount_must_be_positive(cls, val: Decimal) -> Decimal:
        # Проверка значения (должно быть больше нуля)
        if val <= 0:
            raise ValueError('Amount must be positive')

        return val

    @field_validator('wallet_name')
    def wallet_name_not_empty(cls, val: str) -> str:
        # Убираем пробелы по бокам
        val = val.strip()
        # проверяем не пустая ли строка
        if not val:
            raise ValueError('Wallet name cannot be empty')

        return val


class CrateWalletRequest(BaseModel):
    name: str = Field(..., max_length=128)
    initial_balance: Decimal = 0

    currency: CurrencyEnum = CurrencyEnum.AMD  # Устанавливаем значение по умолчанию

    @field_validator('initial_balance')
    def balance_not_negative(cls, val: Decimal) -> Decimal:
        # Проверка значения (должно быть больше нуля)
        if val < 0:
            raise ValueError('Initial balance cannot be negative')

        return val

    @field_validator('name')
    def wallet_name_not_empty(cls, val: str) -> str:
        # Убираем пробелы по бокам
        val = val.strip()
        # проверяем не пустая ли строка
        if not val:
            raise ValueError('Wallet name cannot be empty')

        return val


class UserRequest(BaseModel):
    login: str = Field(..., max_length=128)


class UserResponse(BaseModel):
    model_config = {'from_attributes': True}
    login: str
    id: int


class WalletResponse(BaseModel):
    model_config = {'from_attributes': True}
    id: int
    name: str
    balance: Decimal
    currency: CurrencyEnum


class OperationResponse(BaseModel):
    model_config = {'from_attributes': True}

    id: int
    wallet_id: int
    type: str  # 'income' or 'expense'
    amount: Decimal
    currency: CurrencyEnum
    category: str | None = None
    subcategory: str | None = None
    created_at: datetime  # Форматируем дату в строку для JSON-ответа


class TransferCreateSchema(BaseModel):
    from_wallet_id: int
    to_wallet_id: int
    amount: Decimal

    @field_validator('to_wallet_id')
    def wallets_must_differ(cls, val: int, info) -> int:
        if "from_wallet_id" in info.data and val == info.data["from_wallet_id"]:
            raise ValueError('Same Wallets ids!')
        return val

    @field_validator('amount')
    def amount_gt_zero(cls, val: Decimal) -> Decimal:
        if val <= 0:
            raise ValueError('Amount must be positive')
        return val
