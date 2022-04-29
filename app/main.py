
#import modules
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models
from .routers import post, user, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind = engine)

app = FastAPI() #fastapi instantiation

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credential = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get('/')
def root():
    return {'message': 'Social_Media_FASTAPI'}