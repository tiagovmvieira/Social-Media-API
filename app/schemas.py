from turtle import st
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(BaseModel):
    pass
