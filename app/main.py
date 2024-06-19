from fastapi import FastAPI
from app.routers import database, commande

app = FastAPI()

origins = ["*"]

app.include_router(commande.router, prefix="/commande")
app.include_router(database.router, prefix="/database")
