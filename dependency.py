from fastapi import HTTPException
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.database import SessionLocal
from app.models import User
from app.repository import users as users_repository

security = HTTPBearer()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    login = credentials.credentials
    user = users_repository.get_user(db, login)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    return user
    