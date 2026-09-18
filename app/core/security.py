from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def create_token(
    user_id: int,
    expire_delta: timedelta,
    token_type: str,
) -> str:
    expire = datetime.now(timezone.utc) + expire_delta
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": token_type,
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def create_access_token(user_id: int) -> str:
    return create_token(
        user_id=user_id,
        expire_delta=timedelta(minutes=settings.access_token_expire_minutes),
        token_type="access",
    )


def create_refresh_token(user_id: int) -> str:
    return create_token(
        user_id=user_id,
        expire_delta=timedelta(days=settings.refresh_token_expire_days),
        token_type="refresh",
    )


def decode_access_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        return int(payload["sub"])
    except (JWTError, KeyError, TypeError, ValueError):
        raise ValueError("Invalid token") from None