from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from .. import oauth2


# from sqlalchemy.sql.functions import func
from .. import models, schemas
from ..database import get_db


router = APIRouter(
  prefix='/posts',
  tags=['Posts']
)


@router.get("/", response_model= List[schemas.PostBase])
def get_posts(db: Session = Depends(get_db)):
  posts = db.query(models.Post).all()
  print(posts)
  return posts


@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
  post = db.query(models.Post).filter(models.Post.id==id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
  return {"post": post}

    

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.PostBase)
def createpost(post: schemas.PostBase, db: Session = Depends(get_db), get_current_user: int=
               Depends(oauth2.get_current_user)):
  
  new_post = models.Post(**post.dict())
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post
  
  
# delete a post
@router.delete("/{id}")
def delete_post(id: int,db: Session = Depends(get_db), get_current_user: int=
               Depends(oauth2.get_current_user)):
  deleted_post = db.query(models.Post).filter(models.Post.id==id)
  
  if deleted_post.first() == None:
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='id not found to delete post')
  
  deleted_post.delete()
  db.commit()
  return Response(HTTPException(status_code=status.HTTP_204_NO_CONTENT))


#update post
@router.put('/{id}')
def update_post(id: int, post:schemas.PostBase, db: Session = Depends(get_db),  get_current_user: int=
               Depends(oauth2.get_current_user)):
  update_post = db.query(models.Post).filter(models.Post.id==id)

  if update_post.first() == None:
    raise HTTPException(status_code=status.HTTP_205_RESET_CONTENT, detail='id not found') 
  update_post.update(post.dict())
  db.commit()
  return {"updated_post": update_post.first()}