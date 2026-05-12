from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_session
from app.models.users import User
from app.schemas.users import UserBase, UserList, UserPublic


router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserBase, session: Session = Depends(get_session)):
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=user.password,
        role=user.role,
    )

    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

        return db_user
    except Exception:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='User with this email already exists.',
        )
        
        
        
@router.get('/', response_model=UserList)
def list_users(session: Session = Depends(get_session)):

    users = session.query(User).all()
    return {'users': users}
