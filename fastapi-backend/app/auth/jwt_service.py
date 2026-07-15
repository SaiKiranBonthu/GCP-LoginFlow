from datetime import (datetime, timedelta, timezone)
from jose import jwt, JWTError
from fastapi import HTTPException, status
from app.models.user import User

JWT_SECRET_KEY = (
   "local-development-secret-key"
)
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 60

def create_access_token( user: User ) -> str:
   current_time = datetime.now(
       timezone.utc
   )
   expiration_time = (
       current_time
       + timedelta(
           minutes=JWT_EXPIRATION_MINUTES
       )
   )
   payload = {
       "sub": user.user_id,
       "email": user.email,
       "tenant_id": user.tenant_id,
       "role": user.role,
       "iat": current_time,
       "exp": expiration_time
   }
   return jwt.encode(
       payload,
       JWT_SECRET_KEY,
       algorithm=JWT_ALGORITHM
   )
   
def decode_access_token( token: str ) -> dict:
   try:
       payload = jwt.decode(
           token,
           JWT_SECRET_KEY,
           algorithms=[JWT_ALGORITHM]
       )
       return payload
   except JWTError as error:
       print ("Application JWT validation failed:", error)
       
       raise HTTPException(
           status_code=status.HTTP_401_UNAUTHORIZED,
           detail="Invalid token",
           headers={"WWW-Authenticate": "Bearer"},
       )