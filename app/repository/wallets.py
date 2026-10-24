
from app.database import SessionLocal
from app.models import Wallet
from sqlalchemy.orm import Session
from decimal import Decimal
from app.enum import CurrencyEnum


def is_wallet_exists(db: Session, user_id: int, wallet_name: str) -> bool:
    return db.query(Wallet).filter(Wallet.user_id == user_id, Wallet.name == wallet_name).first() is not None


def add_income(db: Session, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id, Wallet.name == wallet_name).first()
    wallet.balance += amount
    return wallet



def get_wallet_balance_by_name(db: Session, user_id: int, wallet_name: str) -> Wallet:

    wallet = db.query(Wallet).filter(Wallet.user_id == user_id, Wallet.name == wallet_name).first()
    return wallet


def add_expense(db: Session, user_id: int, wallet_name: str, amount: Decimal) -> Wallet:
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id, Wallet.name == wallet_name).first()
    wallet.balance -= amount
    return wallet


def get_all_wallets(db: Session, user_id: int) -> list[Wallet]:
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).all()
    return wallet


def create_wallet(db: Session, user_id: int, wallet_name: str, amount: Decimal, currency: CurrencyEnum) -> Wallet:
    wallet = Wallet(user_id=user_id, name=wallet_name, balance=amount, currency=currency)
    db.add(wallet)
    db.flush()  # Сохраняем изменения в базе данных, чтобы получить ID нового кошелька
    return wallet


def get_wallet_by_id(db: Session, wallet_id: int, user_id: int) -> Wallet | None:
    return db.query(Wallet).filter(Wallet.id == wallet_id, Wallet.user_id == user_id).scalar()