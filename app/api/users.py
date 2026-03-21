from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.repositories import user_repo
from app.core import security

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Enforce unique email
    existing_user = user_repo.get_user_by_email(db, email=str(user.email))
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    hashed_pwd = security.get_password_hash(user.password)
    new_user = user_repo.create_user(db=db, user=user, hashed_password=hashed_pwd)
    return new_user