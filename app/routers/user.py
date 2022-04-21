from fastapi import status, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix = '/users',
    tags = ['Users']
)

@router.post('/', status_code = status.HTTP_201_CREATED, response_model = schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db))-> models.User:
    
    #hashed_password = utils.hash(user.password)
    #user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get('/{id}', response_model = schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db))-> models.User:
    user = db.query(models.User).filter(models.User.user_id == id).first()

    if (not user):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'User with user_id: {} does not exist'.format(id))

    return user

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db))-> Response:
    user = db.query(models.User).filter(models.User.user_id == id)

    if (user.first() is None):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'user with user_id: {} does not exist'.format(id))

    user.delete(synchronize_session = False)
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT) #required to send the 204 status code


