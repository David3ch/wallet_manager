from enum import StrEnum, auto


class CurrencyEnum(StrEnum):
    RUB = auto()
    USD = auto()
    EUR = auto()
    AMD = auto()
    
class OperationType(StrEnum):
    INCOME = auto()
    EXPENSE = auto()
    TRANSFER = auto()