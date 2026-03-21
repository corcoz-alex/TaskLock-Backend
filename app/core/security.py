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

    # Decode it back to a standard string so PostgreSQL can save it
    return hashed_bytes.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Convert both the incoming password and the database hash into bytes
    password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')

    # Let bcrypt do the secure comparison
    return bcrypt.checkpw(password=password_bytes, hashed_password=hashed_password_bytes)


def create_access_token(subject: str | int) -> str:
    """Generates a secure JWT for a given user ID."""

    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "exp": expire,
        "sub": str(subject)
    }

    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt