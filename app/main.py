
#import modules
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Union
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import models

import psycopg2
import time

models.Base.metadata.create_all(bind = engine)

app = FastAPI() #fastapi instantiation

class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True

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

MY_POSTS = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
            {'title': 'favourite foods', 'content': 'I like pizza', 'id': 2}]

def find_post(id: int)-> Union[None, dict]:
    for post in MY_POSTS:
        if (post['id'] == id):
            return post
        else:
            return None

def find_index_post(id: int)-> int:
    for i, post in enumerate(MY_POSTS):
        if (post['id'] == id):
            return i

@app.get('/')
def root() -> dict:
    return {'message': 'Hello World'}

@app.get('/sqlalchemy')
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {'data': posts}

@app.get('/posts')
def get_posts(db: Session = Depends(get_db))-> dict:
    posts = db.query(models.Post).all()

    return {'data': posts}

@app.post('/posts', status_code = status.HTTP_201_CREATED)
def create_posts(post: Post)-> dict:
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
                    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}

@app.get('/posts/latest')
def get_latest_post()-> dict:
    post = MY_POSTS[len(MY_POSTS) - 1]
    return {'detail': post}

@app.get('/posts/{id}')
def get_post(id: int)-> dict:
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if (not post):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'post with id: {} was not found'.format(id))

    return {"post_detail": post}

@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int)-> Response:
    cursor.execute("""DELETE FROM posts WHERE id = %s  RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if (deleted_post is None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'post with id: {} does not exist'.format(id))

    return Response(status_code = status.HTTP_204_NO_CONTENT) #required to send the 204 status code

@app.put('/posts/{id}')
def update_post(id: int, post: Post)-> dict:

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s
                    WHERE id = %s RETURNING *""", 
                    (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if (updated_post is None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'post with id: {} does not exist'.format(id))
    
    return {'data': updated_post}