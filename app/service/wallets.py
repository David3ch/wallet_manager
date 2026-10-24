from fastapi import HTTPException
from app.models import User
from app.schemas import CrateWalletRequest, WalletResponse
from app.repository import wallets as wallets_repository
from app.database import SessionLocal
from sqlalchemy.orm import Session


def get_balance(db: Session, current_user: User, wallet_name: str | None = None):
    # если имя кошелька не указано
    if wallet_name == None:
        wallets = wallets_repository.get_all_wallets(db, current_user.id)
        return {'total_balance': sum([w.balance for w in wallets])}
    # проверка на наличия такого кошелька - существует ли такой кошелек
    if not wallets_repository.is_wallet_exists(db, current_user.id, wallet_name):
        raise HTTPException(
            status_code=404,
            detail=f'Wallet {wallet_name} not found'
        )
    wallet = wallets_repository.get_wallet_balance_by_name(db, current_user.id, wallet_name)
    return {'wallet': wallet.name, 'balance': wallet.balance}


def get_wallets_list(db: Session, current_user: User) -> list[WalletResponse]:
    # список всех кошельков пользователя (нужен фронтенду)
    wallets = wallets_repository.get_all_wallets(db, current_user.id)
    return [WalletResponse.model_validate(w) for w in wallets]


def create_wallet(db: Session, current_user: User, wallet: CrateWalletRequest) -> WalletResponse:
    # Проверяем существует ли такое кошелек
    if wallets_repository.is_wallet_exists(db, current_user.id, wallet.name):
        raise HTTPException(
            status_code=400,
            detail=f'Wallet {wallet.name} is already exists'
        )
    # создаем новый кошелек с балансом 0
    wallet = wallets_repository.create_wallet(db, current_user.id, wallet.name, wallet.initial_balance, wallet.currency)
    db.commit()
    # информация о кошельке
    return WalletResponse.model_validate(wallet)
