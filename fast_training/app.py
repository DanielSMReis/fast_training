from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_training.database import get_session
from fast_training.models import User
from fast_training.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

database = []


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
    db_user = User(username=user.username, password=user.password, email=user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)  # para retornar o db_user juntamente com o id do banco

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


# exercicio: coletando um usuario unico
@app.get('/users/{user_id}', response_model=UserPublic)
def read_one_user(user_id: int):
    user_wt_id = database[user_id - 1]
    return {'username': user_wt_id.username, 'email': user_wt_id.email, 'id': user_wt_id.id}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not Found')
    user_wt_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_wt_id

    return user_wt_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='User not Found')

    del database[user_id - 1]

    return {'message': 'User Deleted'}


# at11827 #5
# criar tabela upgrade_at como solicitado na aula 04


"""
comandos basicos da sessao:

engine = create_engine(Settings().DATABASE_URL) -> cria o poll de conexoes

session = Session(engine) -> cria a sessao

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
