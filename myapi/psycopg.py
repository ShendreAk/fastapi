from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor



app = FastAPI()

class Post(BaseModel):
    title: str 
    body: str
    published: bool
    ratings: int

try:
  conn = psycopg2.connect(database="fastapi", user="postgres", password="ABss1998", host="localhost", port=5432, cursor_factory=RealDictCursor)
  cursor = conn.cursor()
  print("success")
except Exception as error:
  print(error)
  


  
  
@app.get("/")
def root():
    name ='akshay'
    return {"message": "Hello World", 'name': name}

my_posts =[{'title':'title of post 1', 'body':'body of post 1', 'id': 1},
           {'title':'title of post 2', 'body':'body of post 2', 'id': 2},]

@app.get("/posts")
def get_posts():
  cursor.execute("SELECT * FROM posts;")
  posts = cursor.fetchall()
  return {'myposts':posts}

@app.get("/posts/{id}")
def get_post(id: int):
  print(id)
  cursor.execute("select * from posts where id = %s", (str(id)))
  post = cursor.fetchone()
  
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
  return {"post": post}

    

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def createpost(post: Post):
    cursor.execute("insert into posts (title, body, published, ratings ) values(%s, %s, %s, %s) returning *",(post.title, post.body, post.published, post.ratings))
    post = cursor.fetchall()
    conn.commit()
    return { "post": post}
  
  
# delete a post
@app.delete("/posts/{id}")
def delete_post(id: int):
  cursor.execute("delete from posts where id = %s returning *", (str(id)))
  deleted_post = cursor.fetchone()
  conn.commit()
  print(deleted_post)
  if deleted_post == None:
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='id not found to delete post')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
  return {'deleted post': deleted_post}


#update post
@app.put('/posts/{id}')
def update_post(id: int, post:Post):
  cursor.execute("update posts set title = %s, body =%s, published=%s, ratings=%s where id = %s returning *", (post.title, post.body, post.published,post.ratings, str(id)))
  updated_post = cursor.fetchone()
  print(updated_post)
  conn.commit()
  if updated_post == None:
    raise HTTPException(status_code=status.HTTP_205_RESET_CONTENT, detail='id not found') 
      
  return {"updated_post": updated_post}