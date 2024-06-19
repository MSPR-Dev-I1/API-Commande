from fastapi import FastAPI
from app.routers import database

app = FastAPI()

origins = ["*"]

app.include_router(database.router, prefix="/database")
