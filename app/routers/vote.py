from fastapi import Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text
from typing import Optional, List

from ..database import get_db
from .. import schemas, models, oauth2

# router can create a prefix
router = APIRouter(
    prefix="/vote",  # for the path
    tags=["Vote"]  # grouping in doc by category
)


# -- Like/Unlike Requests ------------------------------------------------------
# composite keys: primary keys that spans multiple columns - unique keys

@ router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user)
):

    # check if post exist

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    # check if vote exist for a post_id and user_id

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id
    )

    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote is None:
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()

            return {"message": "successfully added vote"}

        else:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}"
            )

    else:
        if found_vote is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"vote does not exist"
            )

        else:
            vote_query.delete(synchronize_session=False)
            db.commit()

            return {"message": "successfully deleted vote"}


@ router.post("/", status_code=status.HTTP_201_CREATED)
def all_votes(
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user)
):
    pass
