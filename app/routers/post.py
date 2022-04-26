#import modules
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix = '/posts',
    tags = ['Posts']
)

@router.get('/', response_model = List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user))-> models.Post:
    posts = db.query(models.Post).all()

    return posts

@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user))-> models.Post:
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get('/{id}', response_model = schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user))-> models.Post:
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if (not post):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'post with id: {} was not found'.format(id))
    
    if (post.owner_id != user_id.user.id):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = 'Not authorized to perform requested action')

    return post

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user))-> Response:
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_queried = post_query.first()

    if (post_queried is None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'post with id: {} does not exist'.format(id))

    if (post_queried.owner_id != current_user.id):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = 'Not authorized to perform requested action')

    post_queried.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT) #required to send the 204 status code

@router.put('/{id}', response_model = schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user))-> models.Post:
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post_queried = post_query.first()

    if (post_queried is None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'post with id: {} does not exist'.format(id))
    
    if (post.owner_id != current_user.id):
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,
                            detail = 'Not authorized to perform requested action')

    post_query.update(post.dict(), synchronize_session = False)
    db.commit()
    db.refresh(post_query.first())

    return post_query.first()