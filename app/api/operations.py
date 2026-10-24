from fastapi import APIRouter, Depends, HTTPException, Query
from pytest import Session
from app.models import User
from app.schemas import OperationRequest, OperationResponse

from app.service import operations as operations_service
from app.dependency import get_current_user, get_db
from app.schemas import TransferCreateSchema

router = APIRouter()


@router.post('/operations/income', response_model=OperationResponse)
def add_income(operation: OperationRequest, db=Depends(get_db), current_user: User = Depends(get_current_user)):
    return operations_service.add_income(db, current_user, operation)



@router.post('/operations/expense', response_model=OperationResponse)
def add_expence(operation: OperationRequest, db=Depends(get_db), current_user: User = Depends(get_current_user)):
    return operations_service.add_expence(db, current_user, operation)

@router.get('/operations', response_model=list[OperationResponse])
def get_operations_list(wallet_id: int | None = Query(None), date_from: str | None = Query(None), date_to: str | None = Query(None), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return operations_service.get_operations_list(db, user, wallet_id, date_from, date_to)

from sqlalchemy.orm import Session

@router.post('/operations/transfer', response_model=OperationResponse)
def create_transfer(
    payload: TransferCreateSchema,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return operations_service.transfer_between_wallets(
        db=db,
        user_id=user.id,
        from_wallet_id=payload.from_wallet_id,
        to_wallet_id=payload.to_wallet_id,
        amount=payload.amount
    )