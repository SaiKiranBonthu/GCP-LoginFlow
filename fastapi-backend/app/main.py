from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.signup import router as signup_router
from app.routes.tenant import router as tenant_router
from app.routes.auth import router as auth_router
from app.routes.user import router as user_router
from app.routes.marketplace import router as marketplace_router

app = FastAPI(title="Marketplace Hello World")

app.add_middleware(
   CORSMiddleware,
   allow_origins=["http://localhost:4200"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)
app.include_router(signup_router)
app.include_router(tenant_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(marketplace_router)

@app.get("/")
def root():
   return {"message": "Hello World"}