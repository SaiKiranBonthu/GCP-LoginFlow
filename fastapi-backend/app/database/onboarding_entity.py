from datetime import datetime
from sqlalchemy import (DateTime,String)
from sqlalchemy.orm import (Mapped,mapped_column)
from app.database.database import (Base)

class OnboardingSessionEntity(Base):
   __tablename__ = ("onboarding_sessions")

   session_id: Mapped[str] = (
       mapped_column(
           String(36),
           primary_key=True
       )
   )

   procurement_account_id: (Mapped[str]) = (
       mapped_column(
           String(255),
           nullable=False,
           index=True
       )
   )

   obfuscated_user_id: (Mapped[str]) = (
       mapped_column(
           String(255),
           nullable=False
       )
   )

   created_at: Mapped[datetime] = (
       mapped_column(
           DateTime(
               timezone=True
           ),
           nullable=False
       )
   )

   expires_at: Mapped[datetime] = (
       mapped_column(
           DateTime(
               timezone=True
           ),
           nullable=False,
           index=True
       )
   )