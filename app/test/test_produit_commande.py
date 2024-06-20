from fastapi.testclient import TestClient
from app.test.utils import memory_engine
from app import models, actions

from app.main import app

client = TestClient(app)

def test_get_produits_commande(mocker):
    """
        Cas passant (retourne la liste des produits des commandes)
    """
    produits_commande = [{
        "id_produit_commande": 1,
        "id_produit": 1,
        "quantitee": 10,
        "commande_id": 1,
    },
    {
        "id_produit_commande": 2,
        "id_produit": 2,
        "quantitee": 2,
        "commande_id": 1,
    }]
    mocker.patch("sqlalchemy.orm.Session.query", return_value=produits_commande)

    response = client.get("/produit-commande")

    assert response.status_code == 200
    assert response.json() == produits_commande

def test_get_produits_commande_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    response = client.get("/produit-commande")

    assert response.status_code == 500

def test_get_produit_commande(mocker):
    """
        Cas passant (retourne un produit d'une commande)
    """
    db_produit_commande = {
        "id_produit_commande": 1,
        "id_produit": 1,
        "quantitee": 10,
        "commande_id": 1,
    }
    mock_query = mocker.MagicMock()
    mock_query.where.return_value.first.return_value = db_produit_commande
    mocker.patch("sqlalchemy.orm.Session.query", return_value=mock_query)

    response = client.get("/produit-commande/" + str(db_produit_commande['id_produit_commande']))

    assert response.status_code == 200
    assert response.json() == db_produit_commande

def test_get_produit_commande_error_404(mocker):
    """
        Cas non passant (le produit de la commande n'a pas été trouvé)
    """
    db_produit_commande = None
    mock_query = mocker.MagicMock()
    mock_query.where.return_value.first.return_value = db_produit_commande
    mocker.patch("sqlalchemy.orm.Session.query", return_value=mock_query)

    response = client.get("/produit-commande/1")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Produit Commande not found'}

def test_get_produit_commande_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    response = client.get("/produit-commande/1")

    assert response.status_code == 500

def test_post_produit_commande(mocker):
    """
        Cas passant (retourne le produit avec un id)
    """
    new_produit_commande = {
        "id_produit": 1,
        "quantitee": 10,
        "commande_id": 1,
    }
    db_produit_commande = models.ProduitCommande(
        id_produit_commande=1,
        id_produit=new_produit_commande['id_produit'],
        quantitee=new_produit_commande['quantitee'],
        commande_id=new_produit_commande['commande_id'],
    )

    mocker.patch("app.actions.create_produit_commande", return_value=db_produit_commande)

    response = client.post("/produit-commande", json=new_produit_commande)

    assert response.status_code == 201

def test_action_create_produit_commande():
    """
        Test unitaire de la function create produit commande
    """
    database = memory_engine()
    new_produit_commande = models.ProduitCommande(
        id_produit_commande=1,
        id_produit=1,
        quantitee=10,
        commande_id=1,
    )

    db_produit_commande = actions.create_produit_commande(new_produit_commande, database)

    assert isinstance(db_produit_commande, models.ProduitCommande)
    assert db_produit_commande.id_produit_commande is not None

def test_post_produit_commande_error_422():
    """
        Cas non passant (des informations du produit de la commande sont manquants)
    """
    new_produit_commande = {
        "id_produit": 1,
    }

    response = client.post("/produit-commande", json=new_produit_commande)

    assert response.status_code == 422

def test_post_produit_commande_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    new_produit_commande = {
        "id_produit": 1,
        "quantitee": 10,
        "commande_id": 1,
    }
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    response = client.post("/produit-commande", json=new_produit_commande)

    assert response.status_code == 500

def test_delete_produit_commande(mocker):
    """
        Cas passant (retourne l'id du produit commande supprimée)
    """
    db_produit_commande = models.ProduitCommande(
        id_produit_commande=1,
        id_produit=1,
        quantitee=10,
        commande_id=1,
    )
    mocker.patch("app.actions.get_produit_commande", return_value=db_produit_commande)
    mocker.patch("sqlalchemy.orm.Session.delete", return_value=None)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    response = client.delete("/produit-commande/" + str(db_produit_commande.id_produit_commande))

    assert response.status_code == 200
    assert response.json() == {"deleted": db_produit_commande.id_produit_commande}

def test_delete_produit_commande_error_404(mocker):
    """
        Cas non passant (le produit de la commande n'est pas trouvé)
    """
    mocker.patch("app.actions.get_produit_commande", return_value=None)

    response = client.delete("/produit-commande/1")

    assert response.status_code == 404

def test_delete_produit_commande_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    db_produit_commande = models.ProduitCommande(
        id_produit_commande=1,
        id_produit=1,
        quantitee=10,
        commande_id=1,
    )
    mocker.patch("app.actions.get_produit_commande", return_value=db_produit_commande)
    mocker.patch("sqlalchemy.orm.Session.delete", side_effect=Exception("Connection error"))

    response = client.delete("/produit-commande/1")

    assert response.status_code == 500

def test_patch_produit_commande(mocker):
    """
        Cas passant (retourne le produit de la commande mis à jour)
    """
    db_produit_commande = models.ProduitCommande(
        id_produit_commande=1,
        id_produit=1,
        quantitee=10,
        commande_id=1,
    )
    commande_updated = {
        "quantitee": 2,
    }
    mocker.patch("app.actions.get_produit_commande", return_value=db_produit_commande)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    response = client.patch("/produit-commande/"
        + str(db_produit_commande.id_produit_commande), json=commande_updated)

    assert response.status_code == 200
    assert response.json()["quantitee"] == commande_updated["quantitee"]

def test_patch_produit_commande_error_404(mocker):
    """
         Cas non passant (le produit de la commande n'est pas trouvé)
    """
    produit_commande_updated = {
        "quantitee": 3,
    }
    mocker.patch("app.actions.get_produit_commande", return_value=None)

    response = client.patch("/produit-commande/1", json=produit_commande_updated)

    assert response.status_code == 404

def test_patch_produit_commande_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    db_produit_commande = models.ProduitCommande(
        id_produit_commande=1,
        id_produit=1,
        quantitee=10,
        commande_id=1,
    )
    produit_commande_updated = {
        "quantitee": 3,
    }
    mocker.patch("app.actions.get_produit_commande", return_value=db_produit_commande)
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    response = client.patch("/produit-commande/"
        + str(db_produit_commande.id_produit_commande), json=produit_commande_updated)

    assert response.status_code == 500
