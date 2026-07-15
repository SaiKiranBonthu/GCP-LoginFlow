from fastapi import APIRouter
from app.database.tenant_repository import TenantRepository
router = APIRouter(
   prefix="/api/v1",
   tags=["Tenant"]
)

@router.get("/tenants")
def get_all_tenants():
   return TenantRepository.get_all()