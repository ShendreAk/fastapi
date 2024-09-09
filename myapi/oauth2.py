
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from . import schemas, models
from .database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "n3u878ecu8n9inmowjxjnnc938780238h9fy7rfny3c3bqywuqned9un97r57f76gtbyqiuhj5we46gs8hqw9yxbwdx"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp":expire})
  
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def verify_access_token(token: str, credential_exception):
  try:
      payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM) 
      id: str = payload.get('user_id') 
      if id is None:
        raise credential_exception

      token_data = schemas.Token_data(id=id)
      
  except InvalidTokenError:
    raise credential_exception
  return token_data
  
def get_current_user(token: str= Depends(oauth2_scheme),  db: Session=Depends(get_db)):
  credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
  token = verify_access_token(token, credential_exception=credentials_exception)
  user = db.query(models.User).filter(models.User.id == token.id).first()
  return user
    