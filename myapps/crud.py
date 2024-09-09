from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional




app = FastAPI()

class Post(BaseModel):
    title: str 
    body: str
    id: int
    published: bool
    rating: int

  


  
  
@app.get("/")
def root():
    name ='akshay'
    return {"message": "Hello World", 'name': name}

my_posts =[{'title':'title of post 1', 'body':'body of post 1', 'id': 1},
           {'title':'title of post 2', 'body':'body of post 2', 'id': 2},]

@app.get("/posts")
def get_posts():
  
  return {'myposts':my_posts}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    for p in my_posts:
        if p['id'] == int(id):
          print(p['id'])
          post = p
          return {"post": post}
        else:
            # response.status_code = 404
            # post ="post not found"
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    
    

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def createpost(post: Post):
    print(post.model_dump())
    my_posts.append(post.model_dump())
    return { "post": post}
  
  
# delete a post
@app.delete("/posts/{id}")
def delete_post(id: int):
  for i,p in enumerate(my_posts):
    if p['id']==id:
      my_posts.pop(i)
    else:
      raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='id not found to delete post')
  return Response(status_code=status.HTTP_204_NO_CONTENT)


#update post
@app.put('/posts/{id}')
def update_post(id: int, post:Post):
  for i,p in enumerate(my_posts):
    if p['id']==id:
      my_posts[id] = post
      return {'post':p}    
    else:
      raise HTTPException(status_code=status.HTTP_205_RESET_CONTENT, detail='id not found') 
      
  return Response(HTTPException(status_code=status.HTTP_205_RESET_CONTENT)) 
  