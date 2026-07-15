import os


GOOGLE_CLIENT_ID = (
    "870553932901-6ott8e0l3fm8hp1ajfj81ig42ha38166.apps.googleusercontent.com"
)

MARKETPLACE_JWT_AUDIENCE = os.getenv(
   "MARKETPLACE_JWT_AUDIENCE"
)

FRONTEND_URL = os.getenv(
   "FRONTEND_URL",
   "http://localhost:4200"
)