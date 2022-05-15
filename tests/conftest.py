#import modules
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.testclient import TestClient
from app.oauth2 import create_access_token
from app import models
from app.main import app
from app.config import settings
from app.database import Base, get_db


SQLALCHEMY_DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}_test'.format(settings.database_username, settings.database_password,
                                                            settings.database_hostname, settings.database_port, 
                                                            settings.database_name)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

@pytest.fixture()
def database_session():
    Base.metadata.drop_all(bind = engine) # drops tables
    Base.metadata.create_all(bind = engine) # creates tables
    db = TestingSessionLocal() #creates a testing session
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(database_session):
    def override_get_db():
        
        try:
            yield database_session
        finally:
            database_session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app) # runs client


@pytest.fixture
def test_user(client):
    user_data = {'email' : 'hello123@gmail.com',
                'password' : 'password123'}
    res = client.post('/users/', json = user_data)
    
    assert res.status_code == 201 
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['user_id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": 'Bearer {}'.format(token)
    }
    
    return client


@pytest.fixture
def test_posts(test_user, database_session)-> list:
    posts_data = [
        {
            'title': 'Title Post A',
            'content': 'Content Post A',         
            'owner_id': test_user['user_id']
        },
        {
            'title': 'Title Post B',
            'content': 'Content Post B',
            'owner_id': test_user['user_id']
        },
        {
            'title': 'Title Post C',
            'content': 'Content Post C',
            'owner_id': test_user['user_id']
        }
    ]


    def create_post_model(post_data: dict):
        return models.Post(**post_data)

    post_map = map(create_post_model, posts_data)
    post_list = list(post_map)

    database_session.add_all(post_list) #sqlalchemy

    database_session.commit() # commit the changes to the db
    posts = database_session.query(models.Post).all()
    return posts