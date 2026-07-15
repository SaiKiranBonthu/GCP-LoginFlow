from app.models.user import User

class UserRepository:
   _users: dict[str, User] = {}

   @classmethod
   def create(
       cls,
       user: User
   ) -> User:
       cls._users[user.user_id] = user
       return user

   @classmethod
   def get_by_google_id(
       cls,
       google_id: str
   ) -> User | None:
       for user in cls._users.values():
           if user.google_id == google_id:
               return user
       return None

   @classmethod
   def get_by_email(
       cls,
       email: str
   ) -> User | None:
       for user in cls._users.values():
           if user.email.lower() == email.lower():
               return user
       return None

   @classmethod
   def get_by_tenant_id(
       cls,
       tenant_id: str
   ) -> list[User]:
       return [
           user
           for user in cls._users.values()
           if user.tenant_id == tenant_id
       ]

   @classmethod
   def get_all(
       cls
   ) -> list[User]:
       return list(
           cls._users.values()
       )
       
   @classmethod
   def get_by_id(
        cls,
        user_id: str
    ) -> User | None:
        return cls._users.get( user_id )