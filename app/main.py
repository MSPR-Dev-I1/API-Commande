from fastapi import FastAPI, HTTPException
from app.database import create_tables

app = FastAPI()

origins = ["*"]

@app.post("/create-database")
async def create_database():
    """
        Create database
    """
    try:
        create_tables()
        return "database created"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e
