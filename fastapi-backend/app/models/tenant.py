from pydantic import BaseModel

class Tenant(BaseModel):
    tenant_id: str
    organization: str
    plan: str
    subscription_status: str