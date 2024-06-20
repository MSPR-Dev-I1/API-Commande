from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.connexion import get_db
from app import actions, schemas, models


router = APIRouter()

@router.get("", response_model=List[schemas.Commande], tags=["commande"])
async def get_commandes(database: Session = Depends(get_db)):
    """
        Retourne toutes les commandes
    """
    try:
        db_commandes = actions.get_commandes(database)

        return db_commandes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.get("/{id_commande}", response_model=schemas.Commande, tags=["commande"])
async def get_commande(id_commande: int, database: Session = Depends(get_db)):
    """
        Retourne la commande trouvé par son id
    """
    try:
        db_commande = actions.get_commande(id_commande, database)

        if db_commande is None:
            raise HTTPException(status_code=404, detail="Commande not found")

        return db_commande
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.post("", response_model=schemas.Commande, status_code=201, tags=["commande"])
async def post_commande(commande: schemas.CommandeCreate, database: Session = Depends(get_db)):
    """
        Créer une nouvelle commande
    """
    try:
        new_commande = models.Commande(
            date_commande=commande.date_commande,
            montant_total=commande.montant_total,
            payee=commande.payee,
            status_livraison=commande.status_livraison,
            adresse_livraison=commande.adresse_livraison,
            id_client=commande.id_client,
        )
        db_commande = actions.create_commande(new_commande, database)

        return db_commande
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.delete("/{id_commande}", tags=["commande"])
async def delete_commande(id_commande: int, database: Session = Depends(get_db)):
    """
        Supprime une commande
    """
    try:
        db_commande = actions.get_commande(id_commande, database)
        if db_commande is None:
            raise HTTPException(status_code=404, detail="Commande not found")

        actions.delete_commande(db_commande, database)

        return {"deleted": id_commande}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.patch("/{id_commande}", response_model=schemas.Commande, tags=["commande"])
async def patch_commande(id_commande: int,
    commande: schemas.CommandeUpdate, database: Session = Depends(get_db)):
    """
        Met à jour les données de la commande
    """
    try:
        db_commande = actions.get_commande(id_commande, database)
        if db_commande is None:
            raise HTTPException(status_code=404, detail="Commande not found")

        db_commande = actions.update_commande(db_commande, commande, database)

        return db_commande
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e
