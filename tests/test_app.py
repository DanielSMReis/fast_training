from http import HTTPStatus


# Sempre que uma função de teste recebe o parametro client, ele executa esta funcao e retorna o
# TestCliente(app) => vide arquivo de configuração "conftest.py"
def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'hello world'}  # Assert
