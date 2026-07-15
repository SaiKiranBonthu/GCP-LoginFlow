from app.models.tenant import Tenant

class TenantRepository:
    
    _tenants = {}
    
    @classmethod
    def create(cls, tenant: Tenant):
        cls._tenants[tenant.tenant_id] = tenant
        return tenant
    
    @classmethod
    def get(cls, tenant_id: str):
        return cls._tenants.get(tenant_id)
    
    @classmethod
    def get_all(cls):
        return list(cls._tenants.values())