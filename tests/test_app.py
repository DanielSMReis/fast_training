from http import HTTPStatus


# Sempre que uma função de teste recebe o parametro client, ele executa esta funcao e retorna o
# TestCliente(app) => vide arquivo de configuração "conftest.py"
def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'hello world'}  # Assert


"""
def test_update_usr_Unauthorized(client, user):
    response2 = client.put(
        '/users/9',
        json={'username': 'bob', 'email': 'bob@email.com', 'password': 'mypassword'},
    )
    assert response2.status_code == HTTPStatus.FORBIDDEN
"""
