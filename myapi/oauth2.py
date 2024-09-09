# from jose import JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta
from . import schemas

SECRET_KEY = "n3u878ecu8n9inmowjxjnnc938780238h9fy7rfny3c3bqywuqned9un97r57f76gtbyqiuhj5we46gs8hqw9yxbwdx"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp":expire})
  
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

def verify_access_token(token: str, credential_exception):
  payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM) 
  id: str = payload.get('user_id') 
  if id is None:
    raise credential_exception
  token_data = schemas.Token_data(id=id)