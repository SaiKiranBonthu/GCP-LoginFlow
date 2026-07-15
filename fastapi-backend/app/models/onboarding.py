from datetime import datetime
from pydantic import BaseModel

class OnboardingSession(BaseModel):
    session_id: str
    procurement_account_id: str
    obfuscated_user_id: str
    created_at: datetime