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


def test_update_user(client):
    response = client.put('/users/1', json={'username': 'bob', 'email': 'bob@email.com', 'password': 'mypassword'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@email.com',
        'id': 1,
    }

    response2 = client.put('/users/0', json={'username': 'bob', 'email': 'bob@email.com', 'password': 'mypassword'})

    assert response2.status_code == HTTPStatus.NOT_FOUND


def test_read_one_user(client):
    response = client.get('users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [{'email': 'bob@email.com', 'id': 1, 'username': 'bob'}]}


def test_delete_user(client):
    response = client.delete('users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted'}

    response2 = client.delete('users/2')

    assert response2.status_code == HTTPStatus.NOT_FOUND
