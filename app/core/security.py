import secrets
import bcrypt
from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings

ALGORITHM = "HS256"


def get_password_hash(password: str) -> str:
    # bcrypt mathematically requires raw bytes, so we encode the string first
    pwd_bytes = password.encode('utf-8')

    # Generate a random salt and mix it with the password
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)

    # decode it back to a standard string so PostgreSQL can save it
    return hashed_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # convert both the incoming password and the database hash into bytes
    password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')

    # let bcrypt do the secure comparison
    return bcrypt.checkpw(password=password_bytes, hashed_password=hashed_password_bytes)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Generates the short-lived JWT Access Token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Fallback if no delta is provided
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def create_refresh_token() -> str:
    return secrets.token_urlsafe(32)