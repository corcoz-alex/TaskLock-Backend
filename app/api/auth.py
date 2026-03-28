from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.db.database import get_db
from app.repositories import user_repo, auth_repo
from app.core import security
from app.schemas.token import Token, TokenRefreshRequest

router = APIRouter()

@router.post("/login", response_model=Token)
def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)
):
    user = user_repo.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token_str = create_refresh_token()

    expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    auth_repo.create_refresh_token(
        db=db,
        token=refresh_token_str,
        user_id=user.id,
        expires_at=expires_at
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_token(request: TokenRefreshRequest, db: Session = Depends(get_db)):
    db_token = auth_repo.get_refresh_token(db, token=request.refresh_token)
    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if db_token.revoked:
        raise HTTPException(status_code=401, detail="Session has been revoked")
    if db_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token has expired. Please log in again.")

    auth_repo.revoke_refresh_token(db, token=db_token)

    user = db_token.user
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    new_refresh_token_str = create_refresh_token()
    new_expires_at = datetime.now(timezone.utc) + timedelta(days=30)
    auth_repo.create_refresh_token(
        db=db,
        token=new_refresh_token_str,
        user_id=user.id,
        expires_at=new_expires_at
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token_str,
        "token_type": "bearer"
    }