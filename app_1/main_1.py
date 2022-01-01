""" PYTHON API COURSE - using fastAPI

    doc: https://fastapi.tiangolo.com/tutorial/
    github: https://github.com/Sanjeev-Thiyagarajan/fastapi-course
    install: pip install 'fastapi[all]'

CASE: Social Media type Application

===== VIRTUAL ENVIRONMENTS =====================================================

    - isolated environment to be packaged with the project's packages deployed
    - e.g. project -> virtual environment -> installed with fastapi v1.2.1
    - to not conflict with other projects


For MAC, input in terminal:

    create environment = " python3 -m venv fastapi_venv "
    select terminal = " source projects_github/API_Course/fastapi_venv/bin/activate "
    for local doc = " http://127.0.0.1:8000/redoc "

===== MAIN FEATURES ============================================================

CRUD APPLICATION (operation conventions: name in plural)

    [C]REATE: able to create new posts

        POST: to create entity with inputs

        path(s):
    
        '/posts' - @app.post('/posts')

    [R]EAD: able read existing posts

        GET: to retrieve data from api server

        path(s):

        '/posts/:id' - @app.get('/posts') : for specific single post
        '/posts' - @app.get('/posts/{id}') : for all posts

    [U]PDATE: able update/amend existing posts

        PUT: pass all information to update
        PATCH: pass specific fields needed to change

        path(s):

        '/posts/:id' - @app.put('/post/{id}') : update specific post, with all fields
        '/posts/:id' - @app.patch('/post/{id}') : update specific post, with specific fields


    [D]ELETE: able to delete existing posts

        DELETE: to delete entities by id

        path(s):

        '/posts/:id' - @app.delete('/post/{id}')

"""

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# global variable - storing data

my_posts = [
    {
        "title": "title of post 1",
        "content": "content of post 1",
        "id": 1
    },
    {
        "title": "title of post 2",
        "content": "content of post 2",
        "id": 2
    },
    {
        "title": "3rd title for testing",
        "content": "trying to make patch request work",
        "id": 3
    }
]


# schema for requests

class Post(BaseModel):
    """ Pydantic - for schema

    doc: https://pydantic-docs.helpmanual.io/usage/types/
    use: data validation and settings management using python type annotations
    """

    title: str
    content: str
    published: bool = True  # optional field: to bypass required inputs
    rating: Optional[int] = None  # optional field: if not provided default to None


# http requests methods: https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods

# path operation / route

@app.get("/")  # decorator: applied to function using decorator, turning function to path operator
def root():
    """ 
    /           in get is referencing api instance and get http method

    command:    uvicorn main_1:app

    main:       the file main.py (the Python "module").
    app:        the object created inside of main.py with the line app = FastAPI().
    --reload:   make the server restart after code changes. Only use for development.
                    - in production environment, wouldnt need to change code
    """

    return {"message": "welcome to my api!!"}


@app.post("/posts", status_code=status.HTTP_201_CREATED)  # successful created post should return 201 http response
def create_posts(post: Post):
    """ POST request: sends data to api server usually to create something

    base method: def create_posts(payload: dict = Body(...)))
        - extracted fields from body
        - converted to python dictionary
        - stored inside variable 'payload'

    schema      - more efficient way to get all values from the body
                - controls what client can sends with it getting validated
                - ultimately, the client needs to send data in a schema that the api expects

    Post:       Pydantic model:
                - validation of data when front-end send to api server
                - missing field would throw back an error with pydantic
                - convert to dictionary with .dict()
    """
    print(post)

    title = post.title
    content = post.content
    published = post.published

    # assign id to entry

    post_dict = post.dict()

    # alternative is to increment the id:
    # post_dict["id"] = randrange(0, 1_000_000)

    last_id = max([p["id"] for p in my_posts])
    post_dict["id"] = last_id + 1

    my_posts.append(post_dict)

    print(post_dict["title"])

    # when frontend send to backend to create
    # should always return with id, therefore send back post_dict

    return {"new_post": post_dict}


# get post/posts

@app.get("/posts")
def get_posts():
    """ GET request

    /posts:     new url, and if there are duplicated url then the api will
                get the first instance
    """

    return {"data": my_posts}


@app.get("/posts/latest")
def get_latest_post():
    """ GET request (with similar path as get post)

    latest:     variable for fastapi to take it as {id}
                this issue is resolved by order of function
    reminder:   this function must come before get post below to avoid conflict
    """

    latest_post = my_posts[-1]

    return {"detail": latest_post}


@app.get("/posts/{id}")  # id: path parameter (returns as str)
def get_post(
        id: int,  # definition of id to int will automatically convert
        response: Response  # https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
):
    """ GET request (by id)

    {id}:       fastapi extracts id automatically and can return directly into
                function

                for case where {id} does not exist, the api will return a blank
                with response 200 which is incorrect since its an id that is 
                not found
    """

    post = [p for p in my_posts if p.get("id") == id]

    if post == []:

        # best practice
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found"
        )

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}

    return {"post_detail": post}


# delete posts

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    """ DELETE request (by id)

    {id}:       search index of array using id
                deleted posts should come with 204 http status

                for {id} that does not exist, it will return an index of None
                which will cause an error
    """

    index = [i for (i, p) in enumerate(my_posts) if p["id"] == id]

    if index == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist"
        )

    my_posts.pop(index[0])

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update posts

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    """ PUT request (by id)

    {id}:       search by index of post (by id)
    post:       schema is used to ensure the right inputs are fed
    """

    index = [i for (i, p) in enumerate(my_posts) if p["id"] == id]

    if index == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist"
        )

    post_dict = post.dict()
    post_dict["id"] = id

    my_posts[index[0]] = post_dict

    return {"data": post_dict}


class PatchPost(BaseModel):
    # For patch request, all fields are optional

    title: Optional[str]
    content: Optional[str]
    published: bool = True  # optional field: to bypass required inputs
    rating: Optional[int] = None  # optional field: if not provided default to None


@app.patch("/posts/{id}")
def patch_post(id: int, post: PatchPost):
    """ PATCH request (by id)

    {id}:       search by index of post (by id)
    post:       schema is used to ensure the right inputs are fed
    """

    index = [i for (i, p) in enumerate(my_posts) if p["id"] == id]

    if index == []:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist"
        )

    stored_data = my_posts[index[0]]
    stored_model = PatchPost(**stored_data)

    update_data = post.dict(exclude_unset=True)
    update_data["id"] = id

    updated_post = stored_model.copy(update=update_data)
    my_posts[index[0]] = jsonable_encoder(updated_post)

    return {"data": updated_post}
