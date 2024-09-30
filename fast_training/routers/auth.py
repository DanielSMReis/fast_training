from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_training.database import get_session
from fast_training.models import User
from fast_training.schemas import Token
from fast_training.security import create_access_token, get_current_user, verify_password

router = APIRouter(prefix='/auth', tags=['auth'])

T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]


#  Criando rota para login do user
@router.post('/token', response_model=Token)
def login_for_access_token(session: T_Session, form_data: T_OAuth2Form):
    user = session.scalar(select(User).where(User.username == form_data.username))

    if not user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Usuario ou Senha errados')
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Usuario ou Senha errados')

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
def refresh_access_token(user: User = Depends(get_current_user)):
    new_access_token = create_access_token(data={'sub': user.username})

    return {'access_token': new_access_token, 'token_type': 'bearer'}
