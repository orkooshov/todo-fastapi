from fastapi import FastAPI
from app.database.connection import initialize_database
from app.core.config import FastapiConfig
from app.api.api import router


initialize_database()
app = FastAPI(**FastapiConfig.get_fastapi_kwargs())
app.include_router(router)
