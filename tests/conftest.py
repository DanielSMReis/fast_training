import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_training.app import app
from fast_training.database import get_session
from fast_training.models import User, table_registry
from fast_training.security import get_password_hash


@pytest.fixture
def client(session):
    def sobrescreva_get_session():
        return session

    # dependency_overrides troca a injeção da dependencia do banco de dados real, pelo banco alocado em memoria para os testes,
    # é uma função nativa do fastapi
    with TestClient(app) as client:
        app.dependency_overrides[get_session] = sobrescreva_get_session
        yield client

    app.dependency_overrides.clear()


# com essa fixture e uso do "with" o teste rodará ate a linha yield e aguardará a execução da funcao que entrou com parametro "session",
# depois que ela terminar, o codigo retorna e o comando
# drop_all apagará o banco que foi criado em memoria, isolando assim o texte para cada funcao em que a session for requisitada.
@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},  # retira do sqlalchemy junto com sqlite a validação se o teste esta sendo feito
        # na mesma thread da aplicaçãocoisa que nao esta sendo feita, sao duas threads diferentes, incluindo a passagem do poolclass=Staticpool.
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session  # aqui termina o arrange do teste

    table_registry.metadata.drop_all(engine)  # aqui executa o tier dowm, dropando tudo que foi construido


@pytest.fixture
def user(session):
    pwd = 'testPasswrd'
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)
    # Este atributo ainda nao existe no objeto, mas foi criado com o intuito de haver senha "limpa" salva para realização dos testes (Fix_error_400)
    user.clean_password = 'testPasswrd'  # monkey Patch

    return user


@pytest.fixture
def other_user(session):
    pwd = 'testPasswrd'
    user = UserFactory(password=get_password_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)
    # Este atributo ainda nao existe no objeto, mas foi criado com o intuito de haver senha "limpa" salva para realização dos testes (Fix_error_400)
    user.clean_password = 'testPasswrd'  # monkey Patch

    return user


@pytest.fixture
def token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )
    return response.json()['access_token']


# Criando n usuarios no banco
class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'test{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@exemple.com')
