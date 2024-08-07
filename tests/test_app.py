from http import HTTPStatus


# Sempre que uma função de teste recebe o parametro client, ele executa esta funcao e retorna o
# TestCliente(app) => vide arquivo de configuração "conftest.py"
def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'hello world'}  # Assert


def test_create_user(client):
    # envia a resposta POST como cliente, na url user/ e um JSON contendo o schema correto
    response = client.post(
        '/users/',
        json={
            'username': 'testuser',
            'password': 'passtet',
            'email': 'test@test.com',
        },
    )
    # testa a resposta do servidor se ela voltará como status criado e os valores passados no JSON corretamente
    assert response.status_code == HTTPStatus.CREATED
    # verificando se a resposta do JSON fopi retornada corretamente
    assert response.json() == {'username': 'testuser', 'id': 1, 'email': 'test@test.com'}


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [{'username': 'testuser', 'id': 1, 'email': 'test@test.com'}]}
