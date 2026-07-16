# import os
# from dotenv import load_dotenv
# from sqlalchemy import create_engine, URL
# from sqlalchemy.orm import ( DeclarativeBase, sessionmaker)

# load_dotenv()

# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT","5432")
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASSWORD = os.getenv("DB_PASSWORD")

# required_variables = {
#    "DB_HOST": DB_HOST,
#    "DB_NAME": DB_NAME,
#    "DB_USER": DB_USER,
#    "DB_PASSWORD": DB_PASSWORD
# }

# missing_variables = [
#    variable_name
#    for variable_name, value
#    in required_variables.items()
#    if not value
# ]

# if missing_variables:
#    raise RuntimeError(
#        "Missing database environment "
#        "variables: "
#        + ", ".join(
#            missing_variables
#        )
#    )

# # DATABASE_URL = (
# #    f"postgresql+psycopg2://"
# #    f"{DB_USER}:"
# #    f"{DB_PASSWORD}@"
# #    f"{DB_HOST}:"
# #    f"{DB_PORT}/"
# #    f"{DB_NAME}"
# # )

# DATABASE_URL = URL.create(
#    drivername=(
#        "postgresql+psycopg2"
#    ),
#    username=DB_USER,
#    password=DB_PASSWORD,
#    host=DB_HOST,
#    port=int(
#        DB_PORT
#    ),
#    database=DB_NAME
# )

# engine = create_engine(
#    DATABASE_URL,
#    pool_pre_ping=True,
#    pool_size=5,
#    max_overflow=5
# )

# SessionLocal = sessionmaker(
#    bind=engine,
#    autocommit=False,
#    autoflush=False
# )

# class Base(
#    DeclarativeBase
# ):
#    pass

# def get_database():
#    database = SessionLocal()
#    try:
#        yield database
#    finally:
#        database.close()


import os
from dotenv import load_dotenv
from sqlalchemy import (URL,create_engine)
from sqlalchemy.orm import (DeclarativeBase,sessionmaker)

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT","5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")

required_variables = {
   "DB_NAME": DB_NAME,
   "DB_USER": DB_USER,
   "DB_PASSWORD": DB_PASSWORD
}

missing_variables = [
   variable_name
   for variable_name, value
   in required_variables.items()
   if not value
]

if missing_variables:
   raise RuntimeError(
       "Missing database environment variables: "
       + ", ".join(
           missing_variables
       )
   )

if INSTANCE_CONNECTION_NAME:
   # Cloud Run:
   # Cloud SQL is available through
   # a Unix domain socket.
   DATABASE_URL = URL.create(
       drivername=(
           "postgresql+psycopg2"
       ),
       username=DB_USER,
       password=DB_PASSWORD,
       database=DB_NAME,
       query={
           "host": (
               "/cloudsql/"
               + INSTANCE_CONNECTION_NAME
           )
       }
   )
else:
   # Local development:
   # Connect through the Cloud SQL
   # public IP address.
   if not DB_HOST:
       raise RuntimeError(
           "DB_HOST is required "
           "for local database access."
       )

   DATABASE_URL = URL.create(
       drivername=(
           "postgresql+psycopg2"
       ),
       username=DB_USER,
       password=DB_PASSWORD,
       host=DB_HOST,
       port=int(
           DB_PORT
       ),
       database=DB_NAME
   )

engine = create_engine(
   DATABASE_URL,
   pool_pre_ping=True,
   pool_size=5,
   max_overflow=5,
   pool_recycle=1800
)

SessionLocal = sessionmaker(
   bind=engine,
   autocommit=False,
   autoflush=False
)

class Base(
   DeclarativeBase
):
   pass

def get_database():
   database = SessionLocal()
   try:
       yield database
   finally:
       database.close()