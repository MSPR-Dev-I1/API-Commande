from datetime import datetime
from fastapi.testclient import TestClient
from app.test.utils import memory_engine
from app import models, actions
from app.main import app

client = TestClient(app)

def test_get_commandes(mocker):
    """
        Cas passant (retourne la liste de commande)
    """
    commandes = [{
       "id_commande": 1,
        "date_commande": "2023-10-10T10:10:00",
        "montant_total": 23.12,
        "payee": True,
        "status_livraison": "expédiée",
        "adresse_livraison": "9 rue de la Monnaie 59000 Lille",
        "id_client": 1
    }]
    mocker.patch("sqlalchemy.orm.Session.query", return_value=commandes)

    response = client.get("/commande")

    assert response.status_code == 200
    assert response.json() == commandes

def test_get_commandes_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    response = client.get("/commande")

    assert response.status_code == 500

def test_get_commande(mocker):
    """
        Cas passant (retourne une commande)
    """
    db_commande = {
       "id_commande": 1,
        "date_commande": "2023-10-10T10:10:00",
        "montant_total": 23.12,
        "payee": True,
        "status_livraison": "expédiée",
        "adresse_livraison": "9 rue de la Monnaie 59000 Lille",
        "id_client": 1
    }
    mock_query = mocker.MagicMock()
    mock_query.where.return_value.first.return_value = db_commande
    mocker.patch("sqlalchemy.orm.Session.query", return_value=mock_query)

    response = client.get("/commande/" + str(db_commande['id_commande']))

    assert response.status_code == 200
    assert response.json() == db_commande

def test_get_commande_error_404(mocker):
    """
        Cas non passant (la commande n'a pas été trouvée)
    """
    db_commande = None
    mock_query = mocker.MagicMock()
    mock_query.where.return_value.first.return_value = db_commande
    mocker.patch("sqlalchemy.orm.Session.query", return_value=mock_query)

    response = client.get("/commande/1")

    assert response.status_code == 404
    assert response.json() == {'detail': 'Commande not found'}

def test_get_commande_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    response = client.get("/commande/1")

    assert response.status_code == 500

def test_post_commande(mocker):
    """
        Cas passant (retourne la commande avec un id)
    """
    new_commande = {
        "date_commande": "2023-10-10T10:10:00",
        "montant_total": 23.12,
        "payee": True,
        "status_livraison": "expédiée",
        "adresse_livraison": "9 rue de la Monnaie 59000 Lille",
        "id_client": 1
    }
    db_commande = models.Commande(
        id_commande=1,
        date_commande=new_commande['date_commande'],
        montant_total=new_commande['montant_total'],
        payee=new_commande['payee'],
        status_livraison=new_commande['status_livraison'],
        adresse_livraison=new_commande['adresse_livraison'],
        id_client=new_commande['id_client']
    )

    mocker.patch("app.actions.create_commande", return_value=db_commande)

    response = client.post("/commande", json=new_commande)

    assert response.status_code == 201

def test_action_create_commande():
    """
        Test unitaire de la function create commande
    """
    database = memory_engine()
    new_commande = models.Commande(
        date_commande=datetime.now(),
        montant_total=23.12,
        payee=True,
        status_livraison="expédiée",
        adresse_livraison="9 rue de la Monnaie 59000 Lille",
        id_client=1
    )

    db_commande = actions.create_commande(new_commande, database)

    assert isinstance(db_commande, models.Commande)
    assert db_commande.id_commande is not None

def test_post_commande_error_422():
    """
        Cas non passant (des informations de la commande sont manquants)
    """
    new_commande = {
        "payee": True,
        "status_livraison": "expédiée",
        "adresse_livraison": "9 rue de la Monnaie 59000 Lille",
        "id_client": 1
    }

    response = client.post("/commande", json=new_commande)

    assert response.status_code == 422

def test_post_commande_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    new_commande = {
        "date_commande": "2023-10-10T10:10:00",
        "montant_total": 23.12,
        "payee": True,
        "status_livraison": "expédiée",
        "adresse_livraison": "9 rue de la Monnaie 59000 Lille",
        "id_client": 1
    }
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    response = client.post("/commande", json=new_commande)

    assert response.status_code == 500

def test_delete_commande(mocker):
    """
        Cas passant (retourne l'id de la commande supprimée)
    """
    db_commande = models.Commande(
        id_commande=1,
        date_commande=datetime.now(),
        montant_total=23.12,
        payee=True,
        status_livraison="expédiée",
        adresse_livraison="9 rue de la Monnaie 59000 Lille",
        id_client=1
    )
    mocker.patch("app.actions.get_commande", return_value=db_commande)
    mocker.patch("sqlalchemy.orm.Session.delete", return_value=None)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    response = client.delete("/commande/" + str(db_commande.id_commande))

    assert response.status_code == 200
    assert response.json() == {"deleted": db_commande.id_commande}

def test_delete_commande_error_404(mocker):
    """
        Cas non passant (la commande n'est pas trouvée)
    """
    mocker.patch("app.actions.get_commande", return_value=None)

    response = client.delete("/commande/1")

    assert response.status_code == 404

def test_delete_commande_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    db_commande = models.Commande(
        id_commande=1,
        date_commande=datetime.now(),
        montant_total=23.12,
        payee=True,
        status_livraison="expédiée",
        adresse_livraison="9 rue de la Monnaie 59000 Lille",
        id_client=1
    )
    mocker.patch("app.actions.get_commande", return_value=db_commande)
    mocker.patch("sqlalchemy.orm.Session.delete", side_effect=Exception("Connection error"))

    response = client.delete("/commande/1")

    assert response.status_code == 500

def test_patch_commande(mocker):
    """
        Cas passant (retourne la commande mise à jour)
    """
    db_commande = models.Commande(
        id_commande=1,
        date_commande=datetime.now(),
        montant_total=23.12,
        payee=True,
        status_livraison="en préparation",
        adresse_livraison="9 rue de la Monnaie 59000 Lille",
        id_client=1
    )
    commande_updated = {
        "status_livraison": "expédiée",
    }
    mocker.patch("app.actions.get_commande", return_value=db_commande)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    response = client.patch("/commande/" + str(db_commande.id_commande), json=commande_updated)

    assert response.status_code == 200
    assert response.json()["status_livraison"] == commande_updated["status_livraison"]

def test_patch_commande_error_404(mocker):
    """
         Cas non passant (la commande n'est pas trouvée)
    """
    commande_updated = {
        "status_livraison": "expédiée",
    }
    mocker.patch("app.actions.get_commande", return_value=None)

    response = client.patch("/commande/1", json=commande_updated)

    assert response.status_code == 404

def test_patch_commande_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    db_commande = models.Commande(
        id_commande=1,
        date_commande=datetime.now(),
        montant_total=23.12,
        payee=True,
        status_livraison="en préparation",
        adresse_livraison="9 rue de la Monnaie 59000 Lille",
        id_client=1
    )
    commande_updated = {
        "status_livraison": "expédiée",
    }
    mocker.patch("app.actions.get_commande", return_value=db_commande)
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    response = client.patch("/commande/" + str(db_commande.id_commande), json=commande_updated)

    assert response.status_code == 500
