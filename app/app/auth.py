from http import HTTPStatus
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, ExpiredSignatureError
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models.users import User
from app.security import ALGORITHM
from app.settings import settings

oauth2_scheme = HTTPBearer()


def get_current_user(
    session: Session = Depends(get_session),
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = jwt.decode(
            token.credentials,
            settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        subject = payload.get('sub')

        if subject is None:
            raise credentials_exception

        user_id = UUID(subject)

    except DecodeError, ExpiredSignatureError, ValueError:
        raise credentials_exception

    user = session.scalar(select(User).where(User.id == user_id))

    if user is None:
        raise credentials_exception

    return user
