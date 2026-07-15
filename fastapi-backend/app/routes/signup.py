from fastapi import APIRouter
from app.models.signup import SignupRequest
from app.services.signup_service import SignupService
router = APIRouter(
   prefix="/api/v1",
   tags=["Signup"]
)

@router.post("/signup")
def signup(request: SignupRequest):
   return SignupService.process_signup(request)