# from datetime import (
#    datetime,
#    timedelta,
#    timezone
# )
# from app.models.onboarding import (
#    OnboardingSession
# )

# class OnboardingRepository:
#    _sessions: dict[
#        str,
#        OnboardingSession
#    ] = {}

#    SESSION_EXPIRATION_MINUTES = 15

#    @classmethod
#    def create(
#        cls,
#        session: OnboardingSession
#    ) -> OnboardingSession:
#        cls._sessions[
#            session.session_id
#        ] = session
#        return session

#    @classmethod
#    def get(
#        cls,
#        session_id: str
#    ) -> OnboardingSession | None:
#        session = cls._sessions.get(
#            session_id
#        )

#        if not session:
#            return None

#        expiration_time = (
#            session.created_at
#            + timedelta(
#                minutes=(
#                    cls
#                    .SESSION_EXPIRATION_MINUTES
#                )
#            )
#        )

#        current_time = datetime.now(
#            timezone.utc
#        )

#        if current_time > expiration_time:
#            cls._sessions.pop(
#                session_id,
#                None
#            )
#            return None

#        return session

#    @classmethod
#    def delete(
#        cls,
#        session_id: str
#    ) -> None:
#        cls._sessions.pop(
#            session_id,
#            None
#        )
       
       
from datetime import (datetime,timedelta,timezone)
from sqlalchemy import delete
from app.database.database import (SessionLocal)
from app.database.onboarding_entity import (OnboardingSessionEntity)
from app.models.onboarding import (OnboardingSession)

class OnboardingRepository:
   SESSION_EXPIRATION_MINUTES = 15

   @classmethod
   def create(cls,session: OnboardingSession) -> OnboardingSession:
       database = SessionLocal()
       try:
           expires_at = (
               session.created_at
               + timedelta(minutes=(cls.SESSION_EXPIRATION_MINUTES))
           )

           entity = OnboardingSessionEntity(
               session_id=(session.session_id),
               procurement_account_id=(session.procurement_account_id),
               obfuscated_user_id=(session.obfuscated_user_id),created_at=(session.created_at),
               expires_at=(expires_at)
           )

           database.add(entity)

           database.commit()

           return session

       except Exception:
           database.rollback()
           raise

       finally:
           database.close()

   @classmethod
   def get(cls,session_id: str) -> OnboardingSession | None:
       database = SessionLocal()
       try:
           entity = (database.get(OnboardingSessionEntity,session_id))

           if not entity:
               return None

           current_time = datetime.now(timezone.utc)

           expires_at = (entity.expires_at)

           # Some PostgreSQL/driver
           # configurations can return a
           # timezone-naive datetime.
           if (expires_at.tzinfo is None):
               expires_at = (
                   expires_at.replace(tzinfo=timezone.utc)
               )

           if current_time > expires_at:
               database.delete(entity)
               database.commit()
               return None

           return OnboardingSession(
               session_id=(entity.session_id),
               procurement_account_id=(entity.procurement_account_id),
               obfuscated_user_id=(entity.obfuscated_user_id),
               created_at=(entity.created_at)
           )

       finally:
           database.close()

   @classmethod
   def delete(cls,session_id: str) -> None:
       database = SessionLocal()
       try:
           statement = (
               delete(OnboardingSessionEntity)
               .where(OnboardingSessionEntity.session_id== session_id)
           )

           database.execute(statement)

           database.commit()

       except Exception:
           database.rollback()
           raise

       finally:
           database.close()