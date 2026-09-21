import uuid
from typing import Annotated

from database.db import get_db
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.security import decode_access_token
from src.exceptions.auth_exceptions import InvalidTokenError
from src.users.models import User

bearer_scheme = HTTPBearer(auto_error=False)

SessionDep = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
) -> uuid.UUID:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Не авторизован",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        return decode_access_token(credentials.credentials)
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


async def get_current_user(
    session: SessionDep,
    user_id: Annotated[uuid.UUID, Depends(get_current_user_id)],
) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Пользователь не найден")
    if user.is_banned:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Вы были забанены.")
    return user


async def get_current_premium_user(
    user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not user.is_premium:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Эта функция доступна только с premium",
        )
    return user


async def check_if_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Отказано в доступе")
    return user


CurrentUserIdDep = Annotated[uuid.UUID, Depends(get_current_user_id)]
# CurrentUserDep = Annotated[User, Depends(get_current_user)]
# IsAdminDep = Annotated[User, Depends(check_if_admin)]
# PremiumUserDep = Annotated[User, Depends(get_current_premium_user)]


# == MOCK == -delete_after
async def get_current_user_mock(session: SessionDep):
    return await session.get(User, uuid.UUID("01a01c86-5b8e-7d60-a9ff-6dc83ff26276"))


async def get_admin(session: SessionDep):
    return await session.get(User, uuid.UUID("01a01c40-b97b-71e2-948b-06747d91a920"))


async def get_premium_mock(session: SessionDep):
    return await session.get(User, uuid.UUID("01a01c86-5b8e-7d60-a9ff-6dc83ff26276"))


CurrentUserDep = Annotated[User, Depends(get_current_user_mock)]
IsAdminDep = Annotated[User, Depends(get_admin)]
PremiumUserDep = Annotated[User, Depends(get_premium_mock)]
# == MOCK == -delete_after
