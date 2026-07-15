# from fastapi import ( APIRouter, Form, HTTPException)
# from fastapi.responses import ( RedirectResponse )

# router = APIRouter(
#    prefix="/api/v1/marketplace",
#    tags=["Marketplace"]
# )

# @router.post("/signup")
# def marketplace_signup(
#    marketplace_token: str = Form(
#        ...,
#        alias="x-gcp-marketplace-token"
#    )
# ):
#    if not marketplace_token:
#        raise HTTPException(
#            status_code=400,
#            detail=( "Marketplace token is missing.")
#        )

#    print( "Marketplace token received." )

#    print( "Token length:", len( marketplace_token ))

#    return RedirectResponse(
#        url=( "http://localhost:4200/signup" ),
#        status_code=303
#    )


from datetime import ( datetime, timezone )
from uuid import uuid4

from fastapi import ( APIRouter, Form, HTTPException )
from fastapi.responses import ( RedirectResponse )

from app.config import ( FRONTEND_URL, MARKETPLACE_JWT_AUDIENCE)
from app.database.onboarding_repository import ( OnboardingRepository )
from app.marketplace.token_verifier import ( verify_marketplace_token)
from app.models.onboarding import ( OnboardingSession )

router = APIRouter(
   prefix="/api/v1/marketplace",
   tags=["Marketplace"]
)

@router.post("/signup")
def marketplace_signup(
   marketplace_token: str = Form(
       ...,
       alias=(
           "x-gcp-marketplace-token"
       )
   )
):
   try:
       payload = (
           verify_marketplace_token(
               marketplace_token,
               MARKETPLACE_JWT_AUDIENCE
           )
       )

       print( "Marketplace JWT verified successfully." )

       print( "Available JWT claims:", list( payload.keys() ))

       procurement_account_id = (
           payload.get( "account" )
           or
           payload.get( "procurement_account_id" )
       )

       obfuscated_user_id = (
           payload.get( "sub" )
           or
           payload.get( "obfuscated_id" )
       )

       if not ( procurement_account_id ):
           raise HTTPException(
               status_code=400,
               detail=( "Procurement account ID is missing from Marketplace token." )
           )

       if not obfuscated_user_id:
           raise HTTPException(
               status_code=400,
               detail=( "Marketplace user identifier is missing from token." )
           )

       session_id = str( uuid4() )

       session = (
           OnboardingSession(
               session_id=( session_id ),
               procurement_account_id=( procurement_account_id ),
               obfuscated_user_id=( obfuscated_user_id ),
               created_at=( datetime.now(timezone.utc))
           )
       )

       OnboardingRepository.create( session )

       redirect_url = (
           f"{FRONTEND_URL}"
           "/signup"
           f"?session={session_id}"
       )

       return RedirectResponse(
           url=redirect_url,
           status_code=303
       )

   except HTTPException:
       raise

   except ValueError as error:
       print( "Marketplace JWT verification failed:",error )

       raise HTTPException(
           status_code=401,
           detail=str( error )
       )

@router.post("/signup/mock")
def mock_marketplace_signup():
    
   session_id = str(uuid4())
   session = OnboardingSession(session_id=session_id,
       procurement_account_id=("demo-procurement-account"),
       obfuscated_user_id=("demo-marketplace-user"),
       created_at=datetime.now(timezone.utc)
   )
   OnboardingRepository.create(session)
   signup_url = (
       f"{FRONTEND_URL}"
       f"/signup"
       f"?session={session_id}"
   )
   return {
       "message": "Mock Marketplace onboarding session created successfully.",
       "sessionId": session_id,
       "signupUrl":signup_url
   }
   
@router.get(
   "/onboarding/{session_id}"
)
def get_onboarding_session(session_id: str):
   session = (OnboardingRepository.get(session_id))

   if not session:
       raise HTTPException(
           status_code=404,
           detail=("Marketplace onboarding session was not found or has expired.")
       )

   return {
       "valid": True,
       "marketplaceAccount": {
           "procurementAccountId": (session.procurement_account_id)
       }
   }