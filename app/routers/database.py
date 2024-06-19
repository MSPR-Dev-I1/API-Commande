
from fastapi import APIRouter, HTTPException
from app.connexion import create_tables

router = APIRouter()

@router.post("", tags=["database"])
async def create_database():
    """
        Create database
    """
    try:
        create_tables()
        return "database created"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e
