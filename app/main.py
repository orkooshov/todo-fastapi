from fastapi import FastAPI
from fastapi.security import HTTPBearer, OAuth2PasswordBearer
from app.database.connection import initialize_database
from app.core.config import FastapiConfig
from app.api.api import router

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*"
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
http_bearer = HTTPBearer()

initialize_database()
app = FastAPI(**FastapiConfig.get_fastapi_kwargs())
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
