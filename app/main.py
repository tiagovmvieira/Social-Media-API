
#import modules
from email.policy import HTTP
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import List
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .database import engine
from . import models, schemas, utils
from .routers import post, user, auth

import psycopg2
import time


models.Base.metadata.create_all(bind = engine)

app = FastAPI() #fastapi instantiation

while True:
    try:
        conn = psycopg2.connect(host = 'localhost',
                                database = 'Social_Media_FASTAPI',
                                user = 'tiagovieira',
                                password = 'password123',
                                cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print('Database Connection was sucessfull!')
        break
    except Exception as error:
        print('Connection to database failed')
        print('Error:', error)
        time.sleep(3)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)