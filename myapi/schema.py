from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
app = FastAPI()


# Schema using pydantic
# title str, content str

class Post(BaseModel):
    title: str 
    body: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    name ='akshay'
    return {"message": "Hello World", 'name': name}


@app.post('/createposts')
def createpost(post: Post):
    print(post.model_dump())
    return { "post": post}