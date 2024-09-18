from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_training.database import get_session
from fast_training.models import User
from fast_training.schemas import Message, Token, UserList, UserPublic, UserSchema
from fast_training.security import create_access_token, get_password_hash, verify_password

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hello world'}


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
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


@app.get('/users/', response_model=UserList)
def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


"""
# exercicio: coletando um usuario unico
@app.get('/users/{user_id}', response_model=UserPublic)
def read_one_user(user_id: int):
    user_wt_id = database[user_id - 1]
    return {'username': user_wt_id.username, 'email': user_wt_id.email, 'id': user_wt_id.id}

"""


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not Found')

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = get_password_hash(user.password)  # criptografado
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not Found')

    session.delete(db_user)
    session.commit()

    return {'message': 'User Deleted'}


#  Criando rota para login do user
@app.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.username == form_data.username))

    if not user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Email ou Senha errados')
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Email ou Senha errados')

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'bearer'}


# a10615 #6
# falta cobrir as linhas de teste de exercicio do arquivo app.py,
# criar tabela upgrade_at como solicitado na aula 04


"""
comandos basicos da sessao:

engine = create_engine(Settings().DATABASE_URL) -> cria o poll de conexoes

session = Session(engine) -> cria a sessao

  "username": "daniel",
  "email": "daniel@teste.com",
  "password": "senha"

session.add(obj) -> #Adiciona no banco
session.delete(obj) -> remove do banco
session.refresh(obj) -> atualiza o objeco com a sessao

sessio.scarlars(query) -> lista N objetos
session.scarllar(query) -> lista 1 objeto

session.commit() executa as UTs no banco
session.rollback() -> desfas as UTs

session.begin() -> inicia a sessao
session.close() -> fecha a sessao n
"""
