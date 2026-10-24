from app.models import User
from app.service import wallets as wallets_service
from app.schemas import CrateWalletRequest, WalletResponse
from fastapi import APIRouter
from fastapi import Depends

from app.dependency import get_current_user, get_db

router = APIRouter()


@router.get("/balance")
def get_balance(wallet_name: str | None = None, db=Depends(get_db), current_user: User = Depends(get_current_user)):
    return wallets_service.get_balance(db, current_user, wallet_name)



@router.post('/wallets', response_model=WalletResponse)
def create_wallet(wallet: CrateWalletRequest, db=Depends(get_db), current_user: User = Depends(get_current_user)):
    return wallets_service.create_wallet(db, current_user, wallet)