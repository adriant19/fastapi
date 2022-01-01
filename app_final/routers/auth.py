from fastapi import Depends, status, HTTPException, Response, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from .. import schemas, models, utility, oauth2

# router can create a prefix
router = APIRouter(
    prefix="/login",  # for the path
    tags=["Authentication"]  # grouping in doc by category
)


# -- Authentication Requests ---------------------------------------------------

""" LOGGING IN USER

Client -> API : /login {email, password}
API -> dB : find user by email
API <- dB : user {password(hashed)}
API : takes input password, hashes it and check against hashed password
Client <- API : {token}
"""


@ router.post("/", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    # returns username & password which are submitted via form data

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
        )

    if utility.verify_pwd(user_credentials.password, user.password) is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Invalid Credentials"
        )

    # return token

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
