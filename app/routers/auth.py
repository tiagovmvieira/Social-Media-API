from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils

router = APIRouter(
    tags = ['Authentication']
)

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    #check the credentials
    if (not user):
        raise HTTPException(stauts_code = status.HTTP_404_NOT_FOUND,
                            detail = 'Invalid Credentials')

    if (not utils.verify(user_credentials.password, user.password)):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'Invalid Credentials')

    # create a token
    # return token
    return {"token": "example token"}