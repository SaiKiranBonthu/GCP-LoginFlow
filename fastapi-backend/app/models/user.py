from datetime import datetime, timezone
from pydantic import BaseModel, Field

class User(BaseModel):
   user_id: str
   google_id: str
   tenant_id: str
   email: str
   name: str | None = None
   picture: str | None = None
   role: str = "USER"
   created_at: datetime = Field(
       default_factory=lambda: datetime.now(
           timezone.utc
       )
   )