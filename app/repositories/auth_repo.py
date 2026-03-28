from sqlalchemy.orm import Session
from datetime import datetime
from app.db.models import RefreshToken

def create_refresh_token(db: Session, token: str, user_id: int, expires_at: datetime) -> RefreshToken:
    db_token = RefreshToken(token=token, user_id=user_id, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def get_refresh_token(db: Session, token: str) -> RefreshToken | None:
    return db.query(RefreshToken).filter(RefreshToken.token == token).first()

def revoke_refresh_token(db: Session, token: RefreshToken) -> RefreshToken:
    token.revoked = True
    db.commit()
    db.refresh(token)
    return token