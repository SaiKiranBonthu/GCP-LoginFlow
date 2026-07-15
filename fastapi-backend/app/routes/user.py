from fastapi import APIRouter
from app.database.user_repository import (
   UserRepository
)

router = APIRouter(
   prefix="/api/v1",
   tags=["Users"]
)

@router.get("/users")
def get_all_users():
   return (
       UserRepository.get_all()
   )