
#import modules
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from psycopg2.extras import RealDictCursor

from .config import settings

import psycopg2
import time

SQLALCHEMY_DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(settings.database_username, settings.database_password,
                                                            settings.database_hostname, settings.database_port, 
                                                            settings.database_name)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

while True:
    try:
        conn = psycopg2.connect(host = '{}'.format(settings.database_hostname),
                                database = '{}'.format(settings.database_name),
                                user = '{}'.format(settings.database_username),
                                password = '{}'.format(settings.database_password),
                                cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print('Database Connection was sucessfull!')
        break
    except Exception as error:
        print('Connection to database failed')
        print('Error:', error)
        time.sleep(3)
