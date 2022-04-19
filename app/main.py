
#import modules
from email.policy import HTTP
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from typing import Union
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models, schemas

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

@app.get('/')
def root() -> dict:
    return {'message': 'Hello World'}

@app.get('/posts')
def get_posts(db: Session = Depends(get_db))-> dict:
    posts = db.query(models.Post).all()

    return posts

@app.post('/posts', status_code = status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db))-> dict:
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db))-> dict:
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if (not post):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'post with id: {} was not found'.format(id))

    return post

@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db))-> Response:

    post = db.query(models.Post).filter(models.Post.id == id)

    if (post.first() is None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'post with id: {} does not exist'.format(id))

    post.delete(synchronize_session = False)
    db.commit()
    db.refresh(post.first())

    return Response(status_code = status.HTTP_204_NO_CONTENT) #required to send the 204 status code

@app.put('/posts/{id}')
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db))-> dict:
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_queried = post_query.first()

    if (post_queried is None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'post with id: {} does not exist'.format(id))
    
    post_query.update(post.dict(), synchronize_session = False)
    db.commit()
    db.refresh(post_query.first())

    return post_query.first()