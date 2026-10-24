from fastapi import Depends, HTTPException, Query
from app.database import SessionLocal
from app.models import User
from app.schemas import OperationRequest, OperationResponse
from app.repository import wallets as wallets_repository
from sqlalchemy.orm import Session
from app.repository import operations as operations_repository
from app.dependency import get_current_user, get_db
from app.enum import OperationType
from decimal import Decimal

from app.service.exchange_service import get_exchange_rate

def add_income(db: Session,  current_user: User, operation: OperationRequest) -> OperationResponse:
    # Проверяем существует ли кошелек
    if not wallets_repository.is_wallet_exists(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f'Wallet {operation.wallet_name} not found'
        )

    # Добавление дохода к балансу кошелька
    wallet = wallets_repository.add_income(db, current_user.id, operation.wallet_name, operation.amount)
    operation = operations_repository.create_operation(
        db=db, wallet_id=wallet.id, type=OperationType.INCOME, amount=operation.amount, currency=wallet.currency, category=operation.description
    )
    db.commit()
    return OperationResponse.model_validate(operation)


def add_expence(db: Session, current_user: User, operation: OperationRequest) -> OperationResponse:

    # Проверяем существует ли кошелек
    if not wallets_repository.is_wallet_exists(db, current_user.id, operation.wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f'Wallet {operation.wallet_name} not found'
        )

    # Проверяем хватает ли денег в кошельке
    wallet = wallets_repository.get_wallet_balance_by_name(
        db, current_user.id,operation.wallet_name)
    if wallet.balance < operation.amount:
        raise HTTPException(
            status_code=400,
            detail=f'Insufficient funds. Available: {wallet.balance}'
        )
    # Отнимаем сумму расхода из кошелька
    wallet = wallets_repository.add_expense(
        db, current_user.id,operation.wallet_name, operation.amount)
    operation = operations_repository.create_operation(
            db=db, wallet_id=wallet.id, type=OperationType.EXPENSE, amount=operation.amount, currency=wallet.currency, category=operation.description
        )

    db.commit()
    return OperationResponse.model_validate(operation)

def get_operations_list(db: Session, current_user: User, wallet_id: int | None = Query(None), date_from: str | None = Query(None), date_to: str | None = Query(None)) -> list[OperationResponse]:
    if wallet_id:
        wallet = wallets_repository.get_wallet_by_id(db, wallet_id, current_user.id)
        if not wallet:
            raise HTTPException(
                status_code=404,
                detail=f'Wallet with ID {wallet_id} not found'
            )
        wallet_ids = [wallet.id]
    else:
        wallets = wallets_repository.get_all_wallets(db, current_user.id)
        wallet_ids = [wallet.id for wallet in wallets]
    operations = operations_repository.get_operations_list(db, wallet_ids, date_from, date_to)
    result = []
    for operation in operations:
        result.append(OperationResponse.model_validate(operation))
    return result


def transfer_between_wallets(db: Session, user_id: int, from_wallet_id: int, to_wallet_id: int, amount: Decimal) -> OperationResponse:
    from_wallet = wallets_repository.get_wallet_by_id(db, from_wallet_id, user_id)
    to_wallet = wallets_repository.get_wallet_by_id(db, to_wallet_id, user_id)
    
    if not from_wallet or not to_wallet:
        raise HTTPException(
            status_code=404,
            detail='Wallet not found'
        )
    if from_wallet.balance < amount:
        raise HTTPException(
            status_code=400,
            detail=f'Insufficient funds in wallet {from_wallet.name}. Available: {from_wallet.balance} {from_wallet.currency}'
        ) 
        
    target_amount = amount
    exchange_rate = 1.0
    if from_wallet.currency != to_wallet.currency:
        exchange_rate = get_exchange_rate(from_wallet.currency, to_wallet.currency)
        target_amount = round(amount * exchange_rate, 2)
    
    from_wallet.balance = round(from_wallet.balance - amount, 2)
    to_wallet.balance = round(to_wallet.balance + target_amount, 2)
    operation = operations_repository.create_operation(
        db=db, wallet_id=from_wallet.id, type=OperationType.TRANSFER, amount=target_amount, currency=to_wallet.currency, category=f'Transfer to {to_wallet.name}'
    )
    db.add(from_wallet)
    db.add(to_wallet)
    db.add(operation)
    db.commit()
    return OperationResponse.model_validate(operation)