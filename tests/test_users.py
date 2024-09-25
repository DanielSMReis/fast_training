from http import HTTPStatus

from fast_training.schemas import UserPublic


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    # Convertendo o user criado no banco para um UserPublic do pydantic
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}  # para validar este teste fopi necessario importar nas models
    # o método configdict


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': 'bob', 'email': 'bob@exemple.com', 'password': 'mynewpassword'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Sem Permissao'}


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


def test_delete_user(client, user, token):
    response = client.delete(f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User Deleted'}


def test_delete_wrong_user(client, other_user, token):
    response = client.delete(f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Sem Permissao'}
