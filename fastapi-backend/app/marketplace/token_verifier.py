import jwt
from jwt import (
   ExpiredSignatureError,
   InvalidAudienceError,
   InvalidIssuerError,
   InvalidTokenError,
   PyJWKClient
)

GOOGLE_CERTS_URL = (
   "https://www.googleapis.com/"
   "oauth2/v3/certs"
)

ALLOWED_ISSUERS = [
   "https://accounts.google.com",
   "accounts.google.com"
]

google_key_client = PyJWKClient(
   GOOGLE_CERTS_URL
)

def verify_marketplace_token(
   marketplace_token: str,
   expected_audience: str
) -> dict:
   try:
       signing_key = (
           google_key_client
           .get_signing_key_from_jwt( marketplace_token )
       )

       payload = jwt.decode(
           marketplace_token,
           signing_key.key,
           algorithms=[ "RS256" ],
           audience=( expected_audience ),
           issuer=( ALLOWED_ISSUERS )
       )

       return payload

   except ExpiredSignatureError:
       raise ValueError( "Marketplace token has expired." )

   except InvalidAudienceError:
       raise ValueError( "Marketplace token audience is invalid." )

   except InvalidIssuerError:
       raise ValueError( "Marketplace token issuer is invalid." )

   except InvalidTokenError as error:
       raise ValueError( "Marketplace token is invalid: " f"{error}" )