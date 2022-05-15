# import modules
import pytest
from app import schemas
from .database_setup import client, database_session

@pytest.fixture
def test_user(session):
    user_data = {'email' : 'hello123@gmail.com',
                'password' : 'password123'}
    res = client.post('/users', json = user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    print(res.json())

def test_root(client):
    res = client.get('/')
    print(res.json().get('message'))

    assert res.json().get('message') == 'Social_Media_FASTAPI'
    assert res.status_code == 200

def test_create_user(client):
    res = client.post('/users/', json = {'email': 'hello123@gmail.com', 'password': 'password123'})
    new_user = schemas.UserResponse(**res.json())

    assert new_user.email == 'hello123@gmail.com'
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post('/login/', data = {'username': 'hello123@gmail.com', 'password': 'password123'})

    assert res.status_code == 200
