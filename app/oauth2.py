from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from .config import settings
from .database import get_db
from . import schemas, models

""" JWT TOKEN AUTHENTICATION

https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

- secret_key
- algorithm
- expiration time: how long user login remains logged after authentication


User Flow:

Client -> API : /login {username, password} request - verify if credentials are valid
Client <- API : response with {token} - user verified
Client -> API : /posts request with {token} - verify if token is valid
Client <- API : response with data


JWT TOKEN:

header: algorithm, type (metadata)
payload: send information with payload
signature: combination of header, payload and "secret" (will be used to check if token is valid)


PURPOSE OF SIGNATURE

header, payload, secret -> signature
header, signature, payload -> token

[without secret] header, signature (non-updated signature), payload -> incorrect token

token -> API : header, payload, secret to get test signature and check against user signature

"""

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):

    # make copy of original data
    to_encode = data.copy()

    # update data with expiry: current time + expire minutes (with utcnow)
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):

    # if no error, then authenticated successfully

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # from access_token created in auth
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError as e:
        # captures expired tokens
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    # get token from request by user with dependency

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # requests with dependency created on this function
    # will verify access token and return the verified user

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
