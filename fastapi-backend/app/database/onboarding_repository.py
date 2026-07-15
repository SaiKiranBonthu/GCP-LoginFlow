from datetime import (
   datetime,
   timedelta,
   timezone
)
from app.models.onboarding import (
   OnboardingSession
)

class OnboardingRepository:
   _sessions: dict[
       str,
       OnboardingSession
   ] = {}

   SESSION_EXPIRATION_MINUTES = 15

   @classmethod
   def create(
       cls,
       session: OnboardingSession
   ) -> OnboardingSession:
       cls._sessions[
           session.session_id
       ] = session
       return session

   @classmethod
   def get(
       cls,
       session_id: str
   ) -> OnboardingSession | None:
       session = cls._sessions.get(
           session_id
       )

       if not session:
           return None

       expiration_time = (
           session.created_at
           + timedelta(
               minutes=(
                   cls
                   .SESSION_EXPIRATION_MINUTES
               )
           )
       )

       current_time = datetime.now(
           timezone.utc
       )

       if current_time > expiration_time:
           cls._sessions.pop(
               session_id,
               None
           )
           return None

       return session

   @classmethod
   def delete(
       cls,
       session_id: str
   ) -> None:
       cls._sessions.pop(
           session_id,
           None
       )