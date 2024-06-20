from typing import Union
from datetime import datetime
from pydantic import BaseModel

class CommandeBase(BaseModel):
    """
        Classe interface base Commande
    """
    date_commande: datetime
    montant_total: float
    payee: bool
    status_livraison: str
    adresse_livraison: str
    id_client: int

class Commande(CommandeBase):
    """
        Classe interface Commande
    """
    id_commande: int

class CommandeCreate(CommandeBase):
    """
        Classe interface Commande Create
    """

class CommandeUpdate(BaseModel):
    """
        Classe interface Commande Update
    """
    date_commande: Union[datetime, None] = None
    montant_total: Union[float, None] = None
    payee: Union[bool, None] = None
    status_livraison: Union[str, None] = None
    adresse_livraison: Union[str, None] = None
    id_client: Union[int, None] = None

class ProduitCommandeBase(BaseModel):
    """
        Classe interface base Produit Commande
    """
    id_produit: int
    quantitee: int
    commande_id: int

class ProduitCommande(ProduitCommandeBase):
    """
        Classe interface Produit Commande
    """
    id_produit_commande: int


class ProduitCommandeCreate(ProduitCommandeBase):
    """
         Classe interface Produit Commande Create
    """

class ProduitCommandeUpdate(BaseModel):
    """
        Classe interface Produit Commande Update
    """
    id_produit: Union[int, None] = None
    quantitee: Union[int, None] = None
    commande_id: Union[int, None] = None
