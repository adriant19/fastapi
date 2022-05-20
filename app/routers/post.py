from fastapi import Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text
from sqlalchemy import func
from typing import Optional, List

from ..database import get_db
from .. import schemas, models, oauth2

# router can create a prefix
router = APIRouter(
    prefix="/posts",  # for the path
    tags=["Posts"]  # grouping in doc by category
)


# -- Post Requests -------------------------------------------------------------

@ router.get("/", response_model=List[schemas.PostVote])
def get_all_posts(
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user),  # create dependency
    limit: int = 10,  # for query parameter
    offset: int = 0,  # related to pagination
    search: Optional[str] = ""  # for query parameters
):

    # need to specify list of posts, using typing(List)
    # join to get group by of count of votes

    posts = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.title.contains(search)) \
        .limit(limit) \
        .offset(offset) \
        .all()

    # only filter by logged in user post
    # posts = db.query(models.Post).filter(models.Post.user_id == current_user.id).all()

    return posts


@ router.get("/{id}", response_model=schemas.PostVote)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user)  # create dependency
):

    # need .all() or .first() or .one() to commit
    post = db.query(
        models.Post,
        func.count(models.Vote.post_id).label("votes")
    ) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id) \
        .filter(models.Post.id == id) \
        .first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    # only filter by logged in user post
    # if post.user_id != current_user.id:  # check if user owns post
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail=f"Not authorised to perform requested action"
    #     )

    return post


@ router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(
    post: schemas.PostIn,
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user)  # create dependency
):

    new_post = models.Post(
        **post.dict(),  # unwrap obj as dictionary
        user_id=current_user.id  # set user_id as user's id for created post
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@ router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user)  # create dependency
):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:  # check if post exist
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    if post_query.first().user_id != current_user.id:  # check if user owns post
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorised to perform requested action"
        )

    # https://docs.sqlalchemy.org/en/14/orm/session_basics.html
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_404_NOT_FOUND, content=f"post with id: {id} was deleted")


@ router.put("/{id}", response_model=schemas.PostOut)
def update_post(
    id: int,
    post: schemas.PostIn,
    db: Session = Depends(get_db),
    current_user: object = Depends(oauth2.get_current_user)  # create dependency
):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if post_query.first() is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    if post_query.first().user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Not authorised to perform requested action"
        )

    post_query.update(
        post.dict() | {"updated_at": text("current_timestamp")},
        synchronize_session=False
    )

    db.commit()

    return post_query.first()
