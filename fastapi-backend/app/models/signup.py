from pydantic import BaseModel

class SignupRequest(BaseModel):
    marketplaceToken: str