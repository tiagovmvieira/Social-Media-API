#import modules
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.testclient import TestClient
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
    print('my session fixture ran')
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


