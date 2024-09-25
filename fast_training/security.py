from datetime import datetime, timedelta
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from fast_training import settings
from fast_training.database import get_session
from fast_training.models import User
from fast_training.schemas import TokenData
from fast_training.settings import Settings

pwd_context = PasswordHash.recommended()
settings = Settings()  # noqa: F811
# Caminho explicito para a validação do Bearer token JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),  # Injeta Oauth2 e garante que o token foi enviado
):  # Diminuindo o leque de opções de erros que poderiam ocorrer, com a variavel credencials_exception
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Credenciais nao validadas',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')  # username: str garante que o retorno seja uma string
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)  # Criando um token data do username
    except DecodeError:
        raise credentials_exception  # Testando o token JWT valido

    user = session.scalar(select(User).where(User.username == token_data.username))

    if not user:
        raise credentials_exception

    return user
