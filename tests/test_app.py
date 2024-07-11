from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_training.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)  # Arange

    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'hello world'}  # Assert
