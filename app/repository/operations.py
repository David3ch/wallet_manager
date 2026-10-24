from decimal import Decimal
from app.enum import CurrencyEnum
from app.models import Operation
from pytest import Session

def create_operation(db: Session, wallet_id: int, type: str, amount: Decimal, currency: CurrencyEnum, category: str | None = None, subcategory: str | None = None) -> Operation:
    operation = Operation(wallet_id=wallet_id, type=type, amount=amount, currency=currency, category=category, subcategory=subcategory)
    db.add(operation)
    db.flush()  # Сохраняем изменения в базе данных, чтобы получить ID новой операции
    return operation

def get_operations_list(db: Session, wallet_ids: list[int], date_from: str | None = None, date_to: str | None = None) -> list[Operation]:
    query = db.query(Operation).filter(Operation.wallet_id.in_(wallet_ids))
    
    if date_from:
        query = query.filter(Operation.created_at >= date_from)
    if date_to:
        query = query.filter(Operation.created_at <= date_to)
        
    return query.all()