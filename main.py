from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    desc: str
    published: bool = True
    rating: Optional[int] = None


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
async def get_posts():
    return {"data": "A list of posts"}


@app.post("/posts")
def create_post(payload: Post):
    print(payload)
    return {
        "message": f"success, title : {payload.title}, published: {payload.published}"
    }
