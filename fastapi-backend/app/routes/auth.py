# from fastapi import ( APIRouter, HTTPException, status)
# from google.auth.exceptions import (GoogleAuthError)
# from app.auth.google_auth import (verify_google_token)
# from app.models.auth import (GoogleLoginRequest)
# from app.services.auth_service import (AuthService)

# router = APIRouter(
#    prefix="/api/v1/auth",
#    tags=["Authentication"]
# )

# @router.post("/google")
# def google_login(
#    request: GoogleLoginRequest
# ):
#    try:
#        google_user = verify_google_token(
#            request.idToken
#        )

#        if not google_user.get(
#            "email_verified"
#        ):
#            raise HTTPException(
#                status_code=401,
#                detail=(
#                    "Google email is "
#                    "not verified."
#                )
#            )
#         authentication_result = (
#            AuthService
#            .login_or_create_user(
#                google_user
#            )
#          )

#        return {
#            "success": True,
#            "message": (
#                "Google authentication "
#                "successful."
#            ),
#            "user": {
#                "googleId":
#                    google_user.get("sub"),
#                "email":
#                    google_user.get("email"),
#                "name":
#                    google_user.get("name"),
#                "firstName":
#                    google_user.get(
#                        "given_name"
#                    ),
#                "lastName":
#                    google_user.get(
#                        "family_name"
#                    ),
#                "picture":
#                    google_user.get(
#                        "picture"
#                    )
#            }
#        }

#    except HTTPException:
#        raise

#    except (
#        ValueError,
#        GoogleAuthError
#    ) as error:
#        print(
#            "Google token validation "
#            "failed:",
#            error
#        )
#        raise HTTPException(
#            status_code=status.HTTP_401_UNAUTHORIZED,
#            detail=(
#                "Invalid or expired "
#                "Google ID token."
#            )
#        )


from fastapi import (APIRouter, HTTPException, status, Depends)
from google.auth.exceptions import (GoogleAuthError)
from app.auth.google_auth import (verify_google_token)
from app.models.auth import (GoogleLoginRequest)
from app.services.auth_service import (AuthService)
from app.auth.dependencies import (get_current_user)
from app.models.user import User
from app.database.onboarding_repository import (OnboardingRepository)

router = APIRouter(
   prefix="/api/v1/auth",
   tags=["Authentication"]
)

@router.post("/google")
def google_login(
   request: GoogleLoginRequest
):
   try:
       google_user = (
           verify_google_token(request.idToken)
       )

       if not google_user.get("email_verified"):
           raise HTTPException(
               status_code=401,
               detail=("Google email is not verified.")
           )

    #    authentication_result = (
    #        AuthService.login_or_create_user( google_user )
    #    )
       
       onboarding_session = None
       if request.onboardingSessionId:
           onboarding_session = (
               OnboardingRepository.get(
                   request.onboardingSessionId
               )
           )
           if not onboarding_session:
               raise HTTPException(
                   status_code=404,
                   detail=(
                       "Marketplace onboarding session is invalid or has expired."
                   )
               )
       authentication_result = (
           AuthService.login_or_create_user( google_user, onboarding_session )
       )
       
       if request.onboardingSessionId:
              OnboardingRepository.delete(
                request.onboardingSessionId
              )

       return {
           "success": True,
           "message": ( "Google authentication successful."),
           **authentication_result
       }

   except HTTPException:
       raise

   except ( ValueError, GoogleAuthError) as error:
       print( "Google token validation failed:", error)
       raise HTTPException(
           status_code=(status.HTTP_401_UNAUTHORIZED),
           detail=("Invalid or expired Google ID token.")
       )
       

@router.get("/me")
def get_authenticated_user(
   current_user: User = Depends(get_current_user)
):
   return {
       "success": True,
       "user": current_user
   }