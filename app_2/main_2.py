from fastapi import FastAPI, Depends, status, HTTPException, Response
from typing import List
from sqlalchemy.orm import Session

from database import engine, get_db
import schemas  # pydantic models
import models  # sqlalchemy models
import utility

# -- START OF CODE -------------------------------------------------------------
# uvicorn main_2:app --reload


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# -- http requests -------------------------------------------------------------


# -- Post Requests -------------------------------------------------------------

@ app.get("/")
def root():

    return {"msg": "welcome to the api (with sqlalchemy)"}


@ app.get("/posts", response_model=List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db)):

    # need to specify list of posts, using typing(List)
    posts = db.query(models.Post).all()

    return posts


@ app.get("/posts/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):

    # need .all() or .first() or .one() to commit
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    return post


@ app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostOut)
def create_post(post: schemas.PostIn, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@ app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    # https://docs.sqlalchemy.org/en/14/orm/session_basics.html
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_404_NOT_FOUND)


@ app.put("/posts/{id}", response_model=schemas.PostOut)
def update_post(id: int, post: schemas.PostIn, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


# -- User Requests -------------------------------------------------------------

@ app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):

    # check if user already created

    user_query = db.query(models.User).filter(models.User.email == user.email)

    if user_query.first() != None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"user with email: {user.email} already exist"
        )

    user.password = utility.hash(user.password)

    new_user = models.User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@ app.get("/users", response_model=List[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db)):

    # need to specify list of posts, using typing(List)
    users = db.query(models.User).all()

    return users


@ app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):

    # need .all() or .first() or .one() to commit
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )

    return user
