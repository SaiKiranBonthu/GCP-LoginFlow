from app.models.signup import SignupRequest
from app.marketplace.marketplace_client import MarketplaceClient
from app.database.tenant_repository import TenantRepository
from app.models.tenant import Tenant

class SignupService:
    
   @staticmethod
   def process_signup(request: SignupRequest):
       
       account = MarketplaceClient.get_account(request.marketplaceToken)
       
       tenant = Tenant(
            tenant_id=account["accountId"],
            organization=account["organization"],
            plan=account["plan"],
            subscription_status=account["subscriptionState"],
        )
       
       TenantRepository.create(tenant)
       
       return {
           "success": True,
           "tenant": tenant
       }