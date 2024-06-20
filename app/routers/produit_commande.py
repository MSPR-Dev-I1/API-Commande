from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.connexion import get_db
from app import actions, schemas, models

router = APIRouter()

@router.get("", response_model=List[schemas.ProduitCommande], tags=["produit_commande"])
async def get_produits_commande(database: Session = Depends(get_db)):
    """
        Retourne toutes les produits des commandes
    """
    try:
        db_produits = actions.get_produits_commande(database)

        return db_produits
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}") from exc

@router.get("/{id_produit_commande}", response_model=schemas.ProduitCommande,
    tags=["produit_commande"])
async def get_produit_commande(id_produit_commande: int, database: Session = Depends(get_db)):
    """
        Retourne le produit d'une commande trouvé par son id
    """
    try:
        db_produit_commande = actions.get_produit_commande(id_produit_commande, database)

        if db_produit_commande is None:
            raise HTTPException(status_code=404, detail="Produit Commande not found")

        return db_produit_commande
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}") from exc

@router.post("", response_model=schemas.ProduitCommande, status_code=201, tags=["produit_commande"])
async def post_produit_commande(produit_commande: schemas.ProduitCommandeCreate,
    database: Session = Depends(get_db)):
    """
        Ajoute un produit à une commande
    """
    try:
        db_produit_commande = models.ProduitCommande(
            id_produit=produit_commande.id_produit,
            quantitee=produit_commande.quantitee,
            commande_id=produit_commande.commande_id,
        )
        db_produit_commande = actions.create_produit_commande(db_produit_commande, database)

        return db_produit_commande
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}") from exc

@router.delete("/{id_produit_commande}", tags=["produit_commande"])
async def delete_produit_commande(id_produit_commande: int, database: Session = Depends(get_db)):
    """
        Supprime un produit d'une commande
    """
    try:
        db_produit_commande = actions.get_produit_commande(id_produit_commande, database)
        if db_produit_commande is None:
            raise HTTPException(status_code=404, detail="Produit Commande not found")

        actions.delete_produit_commande(db_produit_commande, database)

        return {"deleted": id_produit_commande}
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}") from exc

@router.patch("/{id_produit_commande}", response_model=schemas.ProduitCommande,
    tags=["produit_commande"])
async def patch_produit_commande(id_produit_commande: int,
    produit_commande: schemas.ProduitCommandeUpdate, database: Session = Depends(get_db)):
    """
        Met à jour les données d'un produit d'une commande
    """
    try:
        db_produit_commande = actions.get_produit_commande(id_produit_commande, database)
        if db_produit_commande is None:
            raise HTTPException(status_code=404, detail="Produit Commande not found")

        db_produit_commande = actions.update_produit_commande(db_produit_commande,
            produit_commande, database)

        return db_produit_commande
    except HTTPException as exc:
        raise exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Connection failed: {exc}") from exc
