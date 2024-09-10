from fastapi import APIRouter, HTTPException, status, Depends
from .. import schemas, models, database, oauth2
from sqlalchemy.orm import Session


router = APIRouter(tags=['Votes'])


@router.post("/votes", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Votes ,db: Session=Depends(database.get_db), current_user=Depends(oauth2.get_current_user)):
  print(vote)
  post_exists = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
  if not post_exists:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exists")
  vote_query = db.query(models.Votes).filter(models.Votes.post_id==vote.post_id, models.Votes.user_id==current_user.id)
  exists = vote_query.first()

  if (vote.dir == 1):
    if exists:
      raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail="user already voted")
    
    new_vote = models.Votes(post_id= vote.post_id, user_id = current_user.id)
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)
    return {'message': "successfully added vote"}
  else:
    if not exists:
      print("i am here")
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exists")
    vote_query.delete()
    db.commit()
    return {"message":"successfully deleted vote"}