from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db



router = APIRouter(
  prefix='/posts',
  tags=['Posts']
)


# @router.get("/", response_model= List[schemas.PostOut])
@router.get("/", response_model= List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), 
              limit:int=10, skip:int=0, search:Optional[str]=""):
  # posts = db.query(models.Post).filter(models.Post.user_id==current_user.id).all()
  # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
  # posts = db.query(models.Post).all()
  results = db.query(models.Post, func.count(models.Votes.post_id).label("votes")).join(models.Votes, models.Post.id == models.Votes.post_id, isouter=True).group_by(models.Post.id).all()
  print(results)
  return results


@router.get("/{id}",response_model= schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
  post = db.query(models.Post).filter(models.Post.id==id).first()
  if not post:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='not found')
  # if post.user_id != current_user.id:
  #   raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
  return  post

    

@router.post("/",status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createpost(post: schemas.PostBase, db: Session = Depends(get_db), current_user: int=
               Depends(oauth2.get_current_user)):
  
  print(current_user.id)
  new_post = models.Post(**post.dict(), user_id=current_user.id)
  db.add(new_post)
  db.commit()
  db.refresh(new_post)
  return new_post
  
  
# delete a post
@router.delete("/{id}")
def delete_post(id: int,db: Session = Depends(get_db), current_user: int=
               Depends(oauth2.get_current_user)):
  post = db.query(models.Post).filter(models.Post.id==id)

  if post.first() == None:
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='id not found to delete post')
  if post.first().user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authorizes to take this action')
  post.delete()
  db.commit()
  return HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='successfully deleted')


#update post
@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, post:schemas.PostBase, db: Session = Depends(get_db),  current_user: int=
               Depends(oauth2.get_current_user)):
  post = db.query(models.Post).filter(models.Post.id==id)

  if post.first() == None:
    raise HTTPException(status_code=status.HTTP_205_RESET_CONTENT, detail='id not found') 
  if post.first().user_id != current_user.id:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authorizes to take this action')
  post.update(post.dict())
  db.commit()
  return post.first()