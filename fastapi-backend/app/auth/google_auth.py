from google.auth.transport import requests
from google.oauth2 import id_token
from app.config import GOOGLE_CLIENT_ID

def verify_google_token(
   google_id_token: str
):
   google_user = id_token.verify_oauth2_token(
       google_id_token,
       requests.Request(),
       GOOGLE_CLIENT_ID
   )
   return google_user