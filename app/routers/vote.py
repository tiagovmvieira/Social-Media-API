
#import modules
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix = '/vote',
    tags = ['Vote']
)

@router.post('/', status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user))-> dict:

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if (not post):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = 'post with id {} does not exist'.format(vote.post_id))


    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.user_id)
    found_vote = vote_query.first()

    if (vote.dir == 1):
        if (found_vote):
            raise HTTPException(status_code = status.HTTP_409_CONFLICT,
                                detail = 'user {} has already voted on post {}'.format(current_user.user_id, vote.post_id))
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.user_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "sucessfully added vote"}
    else:
        if (not found_vote):
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                                detail = 'vote does not exist')
        vote_query.delete(synchronize_session = False)
        db.commit()
        return {"message": "sucessfully deleted vote"}