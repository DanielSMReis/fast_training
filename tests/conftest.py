import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_training.app import app
from fast_training.database import get_session
from fast_training.models import table_registry


@pytest.fixture
def client(session):
    def sobrescreva_get_session():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = sobrescreva_get_session
        yield client

    app.dependency_overrides.clear()


# com essa fixture e uso do "with" o texte rodará ate a linha yield e aguardará a execução da funcao que entrou com parametro "session",
# depois que ela terminar, o codigo retorna e o comando
# drop_all apagará o banco que foi criado em memoria, isolando assim o texte para cada funcao em que a session for requisitada.
@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session  # aqui termina o arrange do teste

    table_registry.metadata.drop_all(engine)  # aqui executa o tier dowm, dropando tudo que foi construido
