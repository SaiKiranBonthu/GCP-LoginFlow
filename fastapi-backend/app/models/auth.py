from pydantic import BaseModel

class GoogleLoginRequest(BaseModel):
    idToken: str
    onboardingSessionId:( str | None) = None