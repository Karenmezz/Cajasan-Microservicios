from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from .data import find_user
from .security import (
    ACCESS_TOKEN_EXPIRE_SECONDS,
    create_access_token,
    create_refresh_token,
    decode_token,
    oauth2_scheme,
    revoked_tokens,
)

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = ACCESS_TOKEN_EXPIRE_SECONDS


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    user = find_user(body.username)
    if not user or user["password"] != body.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )
    return TokenResponse(
        access_token=create_access_token(user["username"], user["role"]),
        refresh_token=create_refresh_token(user["username"], user["role"]),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(body: RefreshRequest):
    payload = decode_token(body.refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tipo de token invalido",
        )
    username = payload.get("sub")
    role = payload.get("role")
    return TokenResponse(
        access_token=create_access_token(username, role),
        refresh_token=create_refresh_token(username, role),
    )


@router.post("/logout")
def logout(token=Depends(oauth2_scheme)):
    revoked_tokens.add(token)
    return {"message": "Sesion cerrada"}
