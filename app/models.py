from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String, Integer, DateTime, DECIMAL, Boolean
from sqlalchemy import ForeignKey
from datetime import datetime

# pylint: disable=too-few-public-methods
class Base(DeclarativeBase):
    """
        Classe Model de base SqlAlchemy
    """

# pylint: disable=too-few-public-methods
class Commande(Base):
    """
        Classe Model de la table commande
    """
    __tablename__ = "commande"

    id_commande: Mapped[int] = mapped_column(primary_key=True)
    date_commande: Mapped[datetime] = mapped_column(DateTime)
    montant_total: Mapped[float] = mapped_column(DECIMAL(5, 2))
    payee: Mapped[bool] = mapped_column(Boolean)
    status_livraison: Mapped[str] = mapped_column(String(50))
    adresse_livraison: Mapped[str] = mapped_column(String(255))
    id_client: Mapped[int] = mapped_column(Integer)

    produits_commande: Mapped[List["ProduitCommande"]] \
        = relationship(back_populates="commande", cascade="all, delete-orphan")

# pylint: disable=too-few-public-methods
class ProduitCommande(Base):
    """
        Classe Model de la table produit_commande
    """
    __tablename__ = "produit_commande"
    id_produit_commande: Mapped[int] = mapped_column(primary_key=True)
    id_produit: Mapped[int] = mapped_column(Integer)
    quantitee: Mapped[int] = mapped_column(Integer)
    commande_id: Mapped[int] = mapped_column(ForeignKey("commande.id_commande"))

    commande: Mapped["Commande"] = relationship(back_populates="produits_commande")
