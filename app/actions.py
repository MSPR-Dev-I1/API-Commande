from sqlalchemy.orm import Session
from app import models, schemas

def get_commandes(database: Session):
    """
        Retourne la liste des commandes
    """
    all_commandes = database.query(models.Commande)
    return all_commandes

def get_commande(id_commande: int, database: Session):
    """
        Retourne une commande
    """
    commande = database.query(models.Commande) \
        .where(models.Commande.id_commande == id_commande).first()
    return commande

def create_commande(commande: models.Commande, database: Session):
    """
        Créer et retourne la commande
    """
    database.add(commande)
    database.commit()
    database.refresh(commande)
    return commande

def delete_commande(commande: models.Commande, database: Session):
    """
        Supprime une commande de la base de données
    """
    database.delete(commande)
    database.commit()

def update_commande(db_commande: models.Commande,
    commande: schemas.CommandeUpdate, database: Session):
    """
        Met à jour les données de la commande
    """
    commande_data = commande.model_dump(exclude_unset=True)
    for key, value in commande_data.items():
        setattr(db_commande, key, value)

    database.commit()

    return db_commande
