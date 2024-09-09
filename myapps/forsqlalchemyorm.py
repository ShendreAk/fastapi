from fastapi import FastAPI, Response, status, HTTPException, Depends

from pydantic import BaseModel

from . import models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title: str 
    body: str
    published: bool
    ratings: int
    
class Postresponse(BaseModel):
    title: str 
    body: str
    published: bool
    ratings: int
    class Config:
        from_attributes = True
        
        
class UserInfo(BaseModel):
    username: str
    email: str
    password: str
    
class UserInfoResponse(BaseModel):
    username: str
    email: str
    class Config:
        from_attributes = True


    
  
@app.get("/")
def root():
    name ='akshay'
    return {"message": "Hello World", 'name': name}

from typing import List

@app.get("/posts", response_model= List[Postresponse])
def get_posts(db: Session = Depends(get_db)):
  posts = db.query(models.Post).all()
  print(posts)
  return posts


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id==id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
  return {"post": post}

    

@app.post("/posts",status_code=status.HTTP_201_CREATED, response_model=Postresponse)
def createpost(post: Post, db: Session = Depends(get_db)):
  
  new_post = models.Post(**post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post
  
  
# delete a post
@app.delete("/posts/{id}")
def delete_post(id: int,db: Session = Depends(get_db)):
  deleted_post = db.query(models.Post).filter(models.Post.id==id)
  
  if deleted_post.first() == None:
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='id not found to delete post')
  
  deleted_post.delete()
  db.commit()
  return Response(HTTPException(status_code=status.HTTP_204_NO_CONTENT))


#update post
@app.put('/posts/{id}')
def update_post(id: int, post:Post, db: Session = Depends(get_db)):
  update_post = db.query(models.Post).filter(models.Post.id==id)

  if update_post.first() == None:
    raise HTTPException(status_code=status.HTTP_205_RESET_CONTENT, detail='id not found') 
  update_post.update(post.dict())
  db.commit()
  return {"updated_post": update_post.first()}



# users

@app.get("/users", response_model= List[UserInfoResponse])
def get_users(db: Session = Depends(get_db)):
  users = db.query(models.User).all()
  print(users)
  return users

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserInfoResponse)
def create_user(user: UserInfo, db: Session = Depends(get_db)):
  user_created = models.User(**user.dict())
  if user_created ==None:
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='post not created')
  db.add(user_created)
  db.commit()
  db.refresh(user_created)
  return user_created

@app.delete('/users/{id}', status_code=status.HTTP_204_NO_CONTENT )
def delete_user(id:int, db: Session = Depends(get_db)):
  user = db.query(models.User).filter(models.User.id == id)
  if user.first() == None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='post not deleted')
  user.delete()
  db.commit()
  return user
