from fastapi import ( Depends, HTTPException, status)
from fastapi.security import ( HTTPAuthorizationCredentials, HTTPBearer)
from app.auth.jwt_service import ( decode_access_token )
from app.database.user_repository import ( UserRepository)
from app.models.user import User

bearer_scheme = HTTPBearer()

def get_current_user(
   credentials:
       HTTPAuthorizationCredentials
       = Depends(
           bearer_scheme
       )
) -> User:
   token = credentials.credentials

   payload = decode_access_token(
       token
   )

   user_id = payload.get(
       "sub"
   )

   if not user_id:
       raise HTTPException(
           status_code=(
               status.HTTP_401_UNAUTHORIZED
           ),
           detail=(
               "The access token does "
               "not contain a user ID."
           ),
           headers={
               "WWW-Authenticate":
                   "Bearer"
           }
       )

   user = (
       UserRepository.get_by_id(
           user_id
       )
   )

   if not user:
       raise HTTPException(
           status_code=(
               status.HTTP_401_UNAUTHORIZED
           ),
           detail=(
               "Authenticated user "
               "was not found."
           ),
           headers={
               "WWW-Authenticate":
                   "Bearer"
           }
       )

   return user