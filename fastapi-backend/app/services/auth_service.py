from uuid import uuid4
from fastapi import HTTPException
from app.auth.jwt_service import (create_access_token)
from app.database.tenant_repository import (TenantRepository)
from app.database.user_repository import (UserRepository)
from app.models.onboarding import (OnboardingSession)
from app.models.tenant import (Tenant)
from app.models.user import (User)

class AuthService:
   @staticmethod
   def login_or_create_user(
       google_user: dict,
       onboarding_session: OnboardingSession | None
   ) -> dict:
       # ---------------------------------
       # Step 1: Read verified Google data
       # ---------------------------------
       google_id = google_user.get("sub")
       email = google_user.get("email")
       name = google_user.get("name")
       picture = google_user.get("picture")

       # ---------------------------------
       # Step 2: Validate required claims
       # ---------------------------------
       if not google_id or not email:
           raise HTTPException(
               status_code=401,
               detail=("Required Google user information is missing.")
           )

       # ---------------------------------
       # Step 3: Check whether the Google
       # user already exists
       # ---------------------------------
       existing_user = (UserRepository.get_by_google_id(google_id))

       if existing_user:
           access_token = (create_access_token(existing_user))

           return {
               "accessToken":access_token,
               "tokenType":"bearer",
               "user":existing_user
           }

       # ---------------------------------
       # Step 4: New users must arrive
       # through Marketplace onboarding
       # ---------------------------------
       if not onboarding_session:
           # Check by email as a fallback.
           #
           # This is useful if the user was
           # already registered but their
           # Google identity lookup did not
           # return a match.
           existing_email_user = (UserRepository.get_by_email(email))

           if existing_email_user:
               access_token = (create_access_token(existing_email_user))

               return {
                   "accessToken":access_token,
                   "tokenType":"bearer",
                   "user":existing_email_user
               }

           raise HTTPException(
               status_code=403,
               detail=("No Marketplace onboarding session was provided. Complete Marketplace setup before signing in.")
           )

       # ---------------------------------
       # Step 5: Get the procurement
       # account from onboarding session
       # ---------------------------------
       tenant_id = (onboarding_session.procurement_account_id)

       if not tenant_id:
           raise HTTPException(
               status_code=400,
               detail=("The Marketplace onboarding session does not contain a procurement account ID.")
           )

       # ---------------------------------
       # Step 6: Find or create the tenant
       # ---------------------------------
       tenant = (TenantRepository.get(tenant_id))

       if not tenant:
           tenant = Tenant(tenant_id=tenant_id,organization=("Marketplace Customer"),
               plan="PENDING",
               subscription_status=("ACCOUNT_PENDING")
           )

           TenantRepository.create(tenant)

       # ---------------------------------
       # Step 7: Determine the user role
       # ---------------------------------
       tenant_users = (UserRepository.get_by_tenant_id(tenant.tenant_id))

       # The first user registered for the
       # Marketplace tenant becomes ADMIN.
       role = (
           "ADMIN"
           if len(tenant_users) == 0
           else "USER"
       )

       # ---------------------------------
       # Step 8: Create the application
       # user and link it to the tenant
       # ---------------------------------
       new_user = User(user_id=str(uuid4()),
           google_id=google_id,
           tenant_id=(tenant.tenant_id),
           email=email,
           name=name,
           picture=picture,
           role=role
       )

       UserRepository.create(new_user)

       # ---------------------------------
       # Step 9: Create our application JWT
       # ---------------------------------
       access_token = (create_access_token(new_user))

       # ---------------------------------
       # Step 10: Return authentication
       # response to Angular
       # ---------------------------------
       return {
           "accessToken":access_token,
           "tokenType":"bearer",
           "user":new_user,
           "marketplace": {
               "procurementAccountId": (onboarding_session.procurement_account_id),
               "obfuscatedUserId": (onboarding_session.obfuscated_user_id)
           }
       }