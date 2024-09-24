from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_training.database import get_session
from fast_training.models import User
from fast_training.schemas import Message, UserList, UserPublic, UserSchema
from fast_training.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where((User.username == user.username) | (User.email == user.email)))

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Usuario ja existe',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email ja exite',
            )

    hashed_password = get_password_hash(user.password)

    db_user = User(username=user.username, password=hashed_password, email=user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)  # para retornar o db_user juntamente com o id do banco

    return db_user


@router.get('/', response_model=UserList)
def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Sem Permissao')

    current_user.username = user.username
    current_user.email = user.email
    current_user.password = get_password_hash(user.password)  # criptografado
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    if current_user.id != user_id:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='Sem Permissao')

    session.delete(current_user)
    session.commit()

    return {'message': 'User Deleted'}