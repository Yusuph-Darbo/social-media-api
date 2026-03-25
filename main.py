from random import randrange
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    desc: str
    published: bool = True
    rating: Optional[int] = None


app = FastAPI()

my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foods", "content": "I like pizza", "id": 2},
]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


@app.post("/posts")
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict["id"] = randrange(0, 10000000000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post_id(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} was not found",
        )
    return {"data": post}
