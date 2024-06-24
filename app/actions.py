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

def get_produits_commande(database: Session):
    """
        Retourne la liste des produits des commandes
    """
    all_produits_commande = database.query(models.ProduitCommande)
    return all_produits_commande

def get_produit_commande(id_produit_commande: int, database: Session):
    """
        Retourne un produit d'une commande
    """
    produit_commande = database.query(models.ProduitCommande) \
        .where(models.ProduitCommande.id_produit_commande == id_produit_commande).first()
    return produit_commande

def create_produit_commande(produit_commande: models.ProduitCommande, database: Session):
    """
        Ajoute un produit à une commande et retourne le produit
    """
    database.add(produit_commande)
    database.commit()
    database.refresh(produit_commande)
    return produit_commande

def delete_produit_commande(produit_commande: models.ProduitCommande, database: Session):
    """
        Supprime un produit d'une commande
    """
    database.delete(produit_commande)
    database.commit()

def update_produit_commande(db_produit_commande: models.ProduitCommande,
    produit_commande: schemas.CommandeUpdate, database: Session):
    """
        Met à jour les données de l'un produit d'une commande
    """
    produit_commande_data = produit_commande.model_dump(exclude_unset=True)
    for key, value in produit_commande_data.items():
        setattr(db_produit_commande, key, value)

    database.commit()

    return db_produit_commande

def get_commandes_client(id_client: int, database: Session):
    """
        Récupére toutes les commandes du client
    """
    commandes = database.query(models.Commande) \
        .where(models.Commande.id_client==id_client).all()
    return commandes

def commandes_non_livrees(database: Session):
    """
        Récupere toutes les commandes non livrées
    """
    commandes = database.query(models.Commande) \
        .where(models.Commande.status_livraison!="livrée").all()

    return commandes
