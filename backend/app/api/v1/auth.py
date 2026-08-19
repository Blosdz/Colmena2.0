from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserRead
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=201)
async def register(payload: RegisterRequest, session: AsyncSession = Depends(get_db)):
    service = AuthService(session)
    user = await service.register(payload)
    return UserRead.model_validate(user)


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, session: AsyncSession = Depends(get_db)):
    service = AuthService(session)
    token = await service.login(payload)
    return TokenResponse(access_token=token)


@router.post("/demo-access", response_model=TokenResponse)
async def demo_access(request: Request, session: AsyncSession = Depends(get_db)):
    settings = get_settings()
    client_host = request.client.host if request.client else ""
    is_loopback = client_host in {"127.0.0.1", "::1", "localhost"}
    if settings.environment == "production" or not settings.demo_access_enabled or not is_loopback:
        raise AuthenticationError("El acceso demo local no está disponible.")

    service = AuthService(session)
    token = await service.login_demo(settings.demo_user_email)
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserRead)
async def me(current_user: User = Depends(get_current_user)):
    return UserRead.model_validate(current_user)
