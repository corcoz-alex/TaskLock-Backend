from sqlalchemy.orm import Session
from app.db.models import User
from app.schemas.user import UserCreate

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def create_user (db: Session, user: UserCreate, hashed_password: str) -> User:
    """Inserts a new user into the databased"""
    db_user = User(
        email=str(user.email),
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user