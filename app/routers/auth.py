from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.app.auth import get_current_user
from app.database import get_session
from app.models.users import User
from app.schemas.auth import LoginRequest, Token
from app.schemas.users import UserPublic
from app.security import (
    create_access_token,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login', response_model=Token)
def login(
    credentials: LoginRequest,
    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == credentials.email))

    if not user or not verify_password(
        credentials.password, user.password_hash
    ):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid email or password',
        )

    token = create_access_token(subject=str(user.id))

    return {
        'access_token': token,
        'token_type': 'bearer',
    }


@router.get('/me', response_model=UserPublic)
def read_current_user(
    user: User = Depends(get_current_user),
):
    return user
