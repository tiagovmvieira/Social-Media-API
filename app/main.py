
#import modules
from fastapi import FastAPI
from pydantic import BaseSettings

from .database import engine
from . import models
from .routers import post, user, auth

class Settings(BaseSettings):
    database_password: str = 'localhost'
    database_username: str = 'postgres'
    secret_key: str = '12eq03209420'

models.Base.metadata.create_all(bind = engine)

app = FastAPI() #fastapi instantiation


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)