from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_training.database import get_session
from fast_training.models import User
from fast_training.schemas import Message, Token
from fast_training.security import create_access_token, verify_password

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hello world'}


#  Criando rota para login do user
@app.post('/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.username == form_data.username))

    if not user:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Usuario ou Senha errados')
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Email ou Senha errados')

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'bearer'}


# a1609 #7
# falta cobrir as linhas de teste de exercicio do arquivo app.py,
# criar tabela upgrade_at como solicitado na aula 04


"""
Exercicios aula 6:
Faça um teste para cobrir o cenário que levanta exception credentials_exception na autenticação caso o User não seja encontrado. Ao olhar a cobertura
de security.py você vai notar que esse contexto não está coberto.

Reveja os testes criados até a aula 5 e veja se eles ainda fazem sentido (testes envolvendo 400)
"""


# ----------------------------------------
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
