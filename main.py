
#import modules
from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI() #fastapi instantiation

class Post(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    rating: Optional[int] = None

MY_POSTS = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},
            {'title': 'favourite foods', 'content': 'I like pizza', 'id': 2}]

@app.get('/')
def root():
    return {'message': 'Hello World'}

@app.get('/posts')
def get_posts():
    return {'data': MY_POSTS}

@app.post('/posts')
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    MY_POSTS.append(post_dict)
    return {"data": post_dict}
