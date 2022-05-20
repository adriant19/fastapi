from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from .config import settings

from . import models
from .routers import post, user, auth, vote


# -- START OF CODE -------------------------------------------------------------
# uvicorn app_final.main:app --reload

# command to tell sqlalchemy to run create statement to generate tables
# can remove if using alembic
# models.Base.metadata.create_all(bind=engine)

# create app
app = FastAPI()

""" Cross-Origin Resource Sharing (CORS)
https://fastapi.tiangolo.com/tutorial/cors/

- frontend running in a browser has JavaScript code that communicates with a 
backend, and the backend is in a different "origin" than the frontend
- CORS allows us to make requests from a web browser on one domain to a server
on a different domain
- By default, API will only allow web browsers running on the same domain as our
server to make requests to it
- before requests are made, it passes through the middleware

e.g. fetch("http://localhost:8000/").then(res=>res.json()).then(console.log)
"""

origins = [
    "https://www.google.com",
    "*"  # wildcard to allow every domain to access
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # can limit by e.g. GET requests only
    allow_headers=["*"],
)

# import router objects from files

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# -- HTTP Requests -------------------------------------------------------------

@ app.get("/")
def root():

    return {"msg": "welcome to the api (with sqlalchemy)"}
