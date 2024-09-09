from jose import JWTError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta

SECRET_KEY = "n3u878ecu8n9inmowjxjnnc938780238h9fy7rfny3c3bqywuqned9un97r57f76gtbyqiuhj5we46gs8hqw9yxbwdx"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
  to_encode = data.copy()
  expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  to_encode.update({"exp":expire})
  
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt