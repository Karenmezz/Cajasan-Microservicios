from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

SECRET_KEY = "cajasan-secret-key-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 180
REFRESH_TOKEN_EXPIRE_SECONDS = 86400

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

revoked_tokens = set()


def create_token(username, role, token_type, expires_in):
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "role": role,
        "type": token_type,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(username, role):
    return create_token(username, role, "access", ACCESS_TOKEN_EXPIRE_SECONDS)


def create_refresh_token(username, role):
    return create_token(username, role, "refresh", REFRESH_TOKEN_EXPIRE_SECONDS)


def decode_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token=Depends(oauth2_scheme)):
    if token in revoked_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token revocado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token invalido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"username": payload.get("sub"), "role": payload.get("role")}
