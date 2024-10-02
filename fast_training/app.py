from http import HTTPStatus

from fastapi import FastAPI

from fast_training.routers import auth, todos, users
from fast_training.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'hello world'}


# a2936 #8
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
poetry add --group dev "packege_name" | para instalar no ambiente de testes apenas

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
