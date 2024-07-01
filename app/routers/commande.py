from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.connexion import get_db
from app import actions, schemas, models, message
from app.routers.auth import verify_authorization

router = APIRouter()

@router.get("", response_model=List[schemas.Commande], tags=["commande"])
async def get_commandes(database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
    """
        Retourne toutes les commandes
    """
    try:
        db_commandes = actions.get_commandes(database)

        return db_commandes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.get('/commande-non-livrees', response_model=List[schemas.Commande], tags=['commande'])
async def commandes_non_livrees(database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
    """
        Retourne la liste de commandes non livrées
    """
    try:
        commandes = actions.commandes_non_livrees(database)
        print(commandes)
        return commandes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.get("/{id_commande}", response_model=schemas.Commande, tags=["commande"])
async def get_commande(id_commande: int, database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
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
async def post_commande(commande: schemas.CommandeCreate, database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
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
async def delete_commande(id_commande: int, database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
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
    commande: schemas.CommandeUpdate, database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
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

@router.get('/client/{id_client}', response_model=List[schemas.Commande], tags=['commande'])
async def get_commandes_client(id_client: int, database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
    """
        Retourne les commandes du client
    """
    try:
        commandes = actions.get_commandes_client(id_client, database)

        return commandes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.post('/{id_commande}/annulation-client', response_model=schemas.Commande, tags=['commande'])
async def annulation_client(id_commande: int, database: Session = Depends(get_db),
                    token = Depends(verify_authorization)):
    """
        Annulation la commande (par un client)
    """
    try:
        db_commande = actions.get_commande(id_commande, database)
        if db_commande is None:
            raise HTTPException(status_code=404, detail="Commande not found")

        if db_commande.status_livraison == "annulée":
            raise HTTPException(status_code=400, detail="Commande déjà annulée")

        if db_commande.status_livraison == "livrée":
            raise HTTPException(status_code=400, detail="La commande est déjà livrée")

        new_commande = schemas.CommandeUpdate(
            status_livraison="annulée",
        )
        db_commande = actions.update_commande(db_commande, new_commande, database)

        if db_commande.payee:
            message.notification_remboursement_commande_client_message(
                db_commande.id_commande, token)

        return db_commande
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.post('/{id_commande}/annulation-preparateur',
    response_model=schemas.Commande, tags=['commande'])
async def annulation_preparateur(id_commande: int, database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
    """
        Annulation la commande (par un préparateur)
    """
    try:
        db_commande = actions.get_commande(id_commande, database)
        if db_commande is None:
            raise HTTPException(status_code=404, detail="Commande not found")

        if db_commande.status_livraison == "annulée":
            raise HTTPException(status_code=400, detail="Commande déjà annulée")

        if db_commande.status_livraison == "livrée":
            raise HTTPException(status_code=400, detail="La commande est déjà livrée")

        new_commande = schemas.CommandeUpdate(
            status_livraison="annulée",
        )
        db_commande = actions.update_commande(db_commande, new_commande, database)

        return db_commande
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.patch('/{id_commande}/changer-statut-commande',
    response_model=schemas.Commande, tags=['commande'])
async def changer_statut_commande(id_commande: int,
    status_livraison: schemas.StatutLivraisonCommande, database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
    """
        Change le status de la commande
    """
    try:
        db_commande = actions.get_commande(id_commande, database)
        if db_commande is None:
            raise HTTPException(status_code=404, detail="Commande not found")

        new_commande = schemas.CommandeUpdate(
            status_livraison=status_livraison.status_livraison,
        )
        db_commande = actions.update_produit_commande(db_commande, new_commande, database)

        return db_commande
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.get('/{id_commande}/montant-commande',
    response_model=schemas.MontantCommande, tags=['commande'])
async def montant_commande(id_commande: int, database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
    """
        Retourne le montant d'une commande
    """
    try:
        db_commande = actions.get_commande(id_commande, database)
        if db_commande is None:
            raise HTTPException(status_code=404, detail="Commande not found")

        db_montant_commande = schemas.MontantCommande(
            montant_total=db_commande.montant_total
        )

        return db_montant_commande
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e

@router.post('/{id_commande}/adresse-livraison', response_model=schemas.Commande, tags=['commande'])
async def adresse_livraison(id_commande: int,
    adresse: schemas.AdresseLivraisonCommande, database: Session = Depends(get_db),
                    _ = Depends(verify_authorization)):
    """
        Ajoute la l'adresse de livraison à la commande
    """
    try:
        db_commande = actions.get_commande(id_commande, database)
        if db_commande is None:
            raise HTTPException(status_code=404, detail="Commande not found")

        new_commande = schemas.CommandeUpdate(
            adresse_livraison=adresse.adresse_livraison
        )

        db_commande = actions.update_produit_commande(db_commande, new_commande, database)

        return db_commande
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Connection failed: {e}") from e
