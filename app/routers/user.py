from fastapi import Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import text
from typing import Optional, List

from ..database import get_db
from .. import schemas, models, utility, oauth2

# router can create a prefix
router = APIRouter(
    prefix="/users",  # for the path
    tags=["Users"]  # grouping in doc by category
)


# -- User Requests -------------------------------------------------------------

@ router.get("/", response_model=List[schemas.UserOut])  # need to specify list of posts, using typing(List)
def get_all_users(db: Session = Depends(get_db)):

    users = db.query(models.User).all()

    return users


@ router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):

    user_query = db.query(models.User).filter(models.User.email == user.email)

    if user_query.first() is not None:  # check if user already created
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"user with email: {user.email} already exist"
        )

    user.password = utility.hash_pwd(user.password)  # overwrite password with hashed
    new_user = models.User(**user.dict())

    db.add(new_user)  # add and commit insert to db table
    db.commit()
    db.refresh(new_user)

    return new_user


@ router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    # need .all() or .first() or .one() to commit
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    return user
