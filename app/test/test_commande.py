from datetime import datetime
from fastapi.testclient import TestClient
from app.test.utils import memory_engine
from app import models, actions
from app.main import app
from app.test.setup import setup_mock_auth

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
        "id_client": 1,
        "produits_commande": []
    }]
    mocker.patch("sqlalchemy.orm.Session.query", return_value=commandes)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.get("/commande",
                           headers=headers)

    assert response.status_code == 200
    assert response.json() == commandes

def test_get_commandes_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.get("/commande",
                           headers=headers)

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
        "id_client": 1,
        "produits_commande": []
    }
    mock_query = mocker.MagicMock()
    mock_query.where.return_value.first.return_value = db_commande
    mocker.patch("sqlalchemy.orm.Session.query", return_value=mock_query)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.get("/commande/" + str(db_commande['id_commande']),
                           headers=headers)

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

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.get("/commande/1",
                           headers=headers)

    assert response.status_code == 404
    assert response.json() == {'detail': 'Commande not found'}

def test_get_commande_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.get("/commande/1",
                           headers=headers)

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

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("/commande", json=new_commande,
                           headers=headers)

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

def test_post_commande_error_422(mocker):
    """
        Cas non passant (des informations de la commande sont manquants)
    """
    new_commande = {
        "payee": True,
        "status_livraison": "expédiée",
        "adresse_livraison": "9 rue de la Monnaie 59000 Lille",
        "id_client": 1
    }

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("/commande", json=new_commande,
                           headers=headers)

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

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("/commande", json=new_commande,
                           headers=headers)

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

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.delete("/commande/" + str(db_commande.id_commande),
                           headers=headers)

    assert response.status_code == 200
    assert response.json() == {"deleted": db_commande.id_commande}

def test_delete_commande_error_404(mocker):
    """
        Cas non passant (la commande n'est pas trouvée)
    """
    mocker.patch("app.actions.get_commande", return_value=None)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.delete("/commande/1",
                           headers=headers)

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

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.delete("/commande/1",
                           headers=headers)

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

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.patch("/commande/" + str(db_commande.id_commande), json=commande_updated,
                           headers=headers)

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

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.patch("/commande/1", json=commande_updated,
                           headers=headers)

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

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.patch("/commande/" + str(db_commande.id_commande), json=commande_updated,
                           headers=headers)

    assert response.status_code == 500

def test_get_commandes_client(mocker):
    """
        Cas passant (retourne les commandes d'un client)
    """
    commandes = [{
        "id_commande": 1,
        "date_commande": "2023-10-10T10:10:00",
        "montant_total": 23.12,
        "payee": True,
        "status_livraison": "expédiée",
        "adresse_livraison": "9 rue de la Monnaie 59000 Lille",
        "id_client": 1,
        "produits_commande": []
    },
    {
        "id_commande": 2,
        "date_commande": "2023-10-11T10:10:00",
        "montant_total": 10.50,
        "payee": False,
        "status_livraison": "en préparation",
        "adresse_livraison": "10 rue de la Monnaie 59000 Lille",
        "id_client": 1,
        "produits_commande": []
    }]
    mock_query = mocker.MagicMock()
    mock_query.where.return_value.all.return_value = commandes
    mocker.patch("sqlalchemy.orm.Session.query", return_value=mock_query)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.get("/commande/client/1",
                           headers=headers)

    assert response.status_code == 200
    for commande in commandes:
        assert commande['id_client'] == 1

def test_get_commandes_client_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.get("/commande/client/1",
                           headers=headers)

    assert response.status_code == 500

def test_get_commandes_non_livrees(mocker):
    """
        Cas passant (retourn toutes les commandes non livrées)    
    """
    commandes = [{
        "id_commande": 1,
        "date_commande": "2023-10-10T10:10:00",
        "montant_total": 23.12,
        "payee": True,
        "status_livraison": "livrée",
        "adresse_livraison": "9 rue de la Monnaie 59000 Lille",
        "id_client": 1,
        "produits_commande": []
    },
    {
        "id_commande": 2,
        "date_commande": "2023-10-11T10:10:00",
        "montant_total": 10.50,
        "payee": False,
        "status_livraison": "livrée",
        "adresse_livraison": "10 rue de la Monnaie 59000 Lille",
        "id_client": 1,
        "produits_commande": []
    }]
    mock_query = mocker.MagicMock()
    mock_query.where.return_value.all.return_value = commandes
    mocker.patch("sqlalchemy.orm.Session.query", return_value=mock_query)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.get("/commande/commande-non-livrees",
                           headers=headers)

    assert response.status_code == 200
    for commande in commandes:
        assert commande['status_livraison'] == 'livrée'

def test_get_commandes_non_livrees_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("sqlalchemy.orm.Session.query", side_effect=Exception("Connection error"))

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.get("/commande/commande-non-livrees",
                           headers=headers)

    assert response.status_code == 500

def test_post_annulation_client(mocker):
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
    mocker.patch("app.actions.get_commande", return_value=db_commande)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    mock_publisher = mocker.MagicMock()
    mock_publisher_topic = mocker.MagicMock()
    mocker.patch("app.message.create_publisher", return_value=mock_publisher)
    mocker.patch("google.cloud.pubsub_v1.PublisherClient.topic_path",
        return_value=mock_publisher_topic)
    mocker.patch("google.cloud.pubsub_v1.PublisherClient.publish", return_value=None)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("commande/" + str(db_commande.id_commande) + "/annulation-client",
                           headers=headers)

    assert response.status_code == 200
    assert response.json()["status_livraison"] == 'annulée'

def test_post_annulation_client_error_404(mocker):
    """
        Cas non passant (ne trouve pas la commande)
    """
    mocker.patch("app.actions.get_commande", return_value=None)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("commande/1/annulation-client",
                           headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Commande not found"}

def test_post_annulation_client_error_400_deja_annulee(mocker):
    """
        Cas non passant (commande déjà annulée)
    """
    db_commande = models.Commande(
        id_commande=1,
        date_commande=datetime.now(),
        montant_total=23.12,
        payee=True,
        status_livraison="annulée",
        adresse_livraison="9 rue de la Monnaie 59000 Lille",
        id_client=1
    )
    mocker.patch("app.actions.get_commande", return_value=db_commande)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("commande/" + str(db_commande.id_commande) + "/annulation-client",
                           headers=headers)

    assert response.status_code == 400
    assert response.json() == {"detail": "Commande déjà annulée"}


def test_post_annulation_client_error_400_deja_livree(mocker):
    """
        Cas non passant (commande déjà livrée)
    """
    db_commande = models.Commande(
        id_commande=1,
        date_commande=datetime.now(),
        montant_total=23.12,
        payee=True,
        status_livraison="livrée",
        adresse_livraison="9 rue de la Monnaie 59000 Lille",
        id_client=1
    )
    mocker.patch("app.actions.get_commande", return_value=db_commande)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("commande/" + str(db_commande.id_commande) + "/annulation-client",
                           headers=headers)

    assert response.status_code == 400
    assert response.json() == {"detail": "La commande est déjà livrée"}

def test_post_annulation_client_error_500(mocker):
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
    mocker.patch("app.actions.get_commande", return_value=db_commande)
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("commande/" + str(db_commande.id_commande) + "/annulation-client",
                           headers=headers)

    assert response.status_code == 500

def test_post_annulation_preparateur(mocker):
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
    mocker.patch("app.actions.get_commande", return_value=db_commande)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("commande/" + str(db_commande.id_commande) + "/annulation-preparateur",
                           headers=headers)

    assert response.status_code == 200
    assert response.json()["status_livraison"] == 'annulée'

def test_post_annulation_preparateur_error_404(mocker):
    """
        Cas non passant (ne trouve pas la commande)
    """
    mocker.patch("app.actions.get_commande", return_value=None)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("commande/1/annulation-preparateur",
                           headers=headers)

    assert response.status_code == 404
    assert response.json() == {"detail": "Commande not found"}

def test_post_annulation_preparateur_error_400_deja_annulee(mocker):
    """
        Cas non passant (commande déjà annulée)
    """
    db_commande = models.Commande(
        id_commande=1,
        date_commande=datetime.now(),
        montant_total=23.12,
        payee=True,
        status_livraison="annulée",
        adresse_livraison="9 rue de la Monnaie 59000 Lille",
        id_client=1
    )
    mocker.patch("app.actions.get_commande", return_value=db_commande)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("commande/" + str(db_commande.id_commande) + "/annulation-preparateur",
                           headers=headers)

    assert response.status_code == 400
    assert response.json() == {"detail": "Commande déjà annulée"}


def test_post_annulation_preparateur_error_400_deja_livree(mocker):
    """
        Cas non passant (commande déjà livrée)
    """
    db_commande = models.Commande(
        id_commande=1,
        date_commande=datetime.now(),
        montant_total=23.12,
        payee=True,
        status_livraison="livrée",
        adresse_livraison="9 rue de la Monnaie 59000 Lille",
        id_client=1
    )
    mocker.patch("app.actions.get_commande", return_value=db_commande)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("commande/" + str(db_commande.id_commande) + "/annulation-preparateur",
                           headers=headers)

    assert response.status_code == 400
    assert response.json() == {"detail": "La commande est déjà livrée"}

def test_post_annulation_preparateur_error_500(mocker):
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
    mocker.patch("app.actions.get_commande", return_value=db_commande)
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("commande/" + str(db_commande.id_commande) + "/annulation-preparateur",
                           headers=headers)

    assert response.status_code == 500

def test_patch_changer_status_commande(mocker):
    """
        Cas passant (Retourne la commande mise à jour)
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
    statut_livraison = {
        "status_livraison": "expédiée"
    }
    mocker.patch("app.actions.get_commande", return_value=db_commande)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.patch("commande/"
        + str(db_commande.id_commande) + "/changer-statut-commande", json=statut_livraison,
                           headers=headers)

    assert response.status_code == 200
    assert response.json()['status_livraison'] == "expédiée"

def test_patch_changer_status_commande_error_400(mocker):
    """
        Cas non passant (Ne trouve pas la commande)
    """
    mocker.patch("app.actions.get_commande", return_value=None)
    statut_livraison = {
        "status_livraison": "expédiée"
    }

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.patch("commande/1/changer-statut-commande", json=statut_livraison,
                           headers=headers)

    assert response.status_code == 404

def test_patch_changer_status_commande_error_500(mocker):
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
    statut_livraison = {
        "status_livraison": "expédiée"
    }
    mocker.patch("app.actions.get_commande", return_value=db_commande)
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.patch("commande/"
        + str(db_commande.id_commande) + "/changer-statut-commande", json=statut_livraison,
                           headers=headers)

    assert response.status_code == 500

def test_get_montant_commande(mocker):
    """
        Cas passant (retourne le montant de la commande)
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
    mocker.patch("app.actions.get_commande", return_value=db_commande)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.get("commande/" + str(db_commande.id_commande) + "/montant-commande",
                           headers=headers)

    assert response.status_code == 200
    assert response.json() == {"montant_total": db_commande.montant_total}

def test_get_montant_commande_error_404(mocker):
    """
        Cas non passant (Ne trouve pas la commande)
    """
    mocker.patch("app.actions.get_commande", return_value=None)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.get("commande/1/montant-commande",
                           headers=headers)

    assert response.status_code == 404

def test_get_montant_commande_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("app.actions.get_commande", side_effect=Exception("Connection error"))

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.get("commande/1/montant-commande",
                           headers=headers)

    assert response.status_code == 500

def test_post_adresse_livraison(mocker):
    """
        Cas passant (retourne la commande mise à jour)
    """
    db_commande = models.Commande(
        id_commande=1,
        date_commande=datetime.now(),
        montant_total=23.12,
        payee=True,
        status_livraison="en préparation",
        adresse_livraison=None,
        id_client=1
    )
    new_commande = {
        "adresse_livraison" : "9 rue de la Monnaie 59000 Lille",
    }
    mocker.patch("app.actions.get_commande", return_value=db_commande)
    mocker.patch("sqlalchemy.orm.Session.commit", return_value=None)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("commande/1/adresse-livraison", json=new_commande,
                           headers=headers)

    assert response.status_code == 200
    assert response.json()['adresse_livraison'] == new_commande['adresse_livraison']

def test_post_adresse_livraison_error_404(mocker):
    """
        Cas non passant (Ne trouve pas la commande)
    """
    new_commande = {
        "adresse_livraison" : "9 rue de la Monnaie 59000 Lille",
    }
    mocker.patch("app.actions.get_commande", return_value=None)

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("commande/1/adresse-livraison", json=new_commande,
                           headers=headers)

    assert response.status_code == 404

def test_post_adresse_livraison_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    db_commande = models.Commande(
        id_commande=1,
        date_commande=datetime.now(),
        montant_total=23.12,
        payee=True,
        status_livraison="en préparation",
        adresse_livraison=None,
        id_client=1
    )
    new_commande = {
        "adresse_livraison" : "9 rue de la Monnaie 59000 Lille",
    }
    mocker.patch("app.actions.get_commande", return_value=db_commande)
    mocker.patch("sqlalchemy.orm.Session.commit", side_effect=Exception("Connection error"))

    setup_mock_auth(mocker)

    headers = {"token": "None"}
    response = client.post("commande/1/adresse-livraison", json=new_commande,
                           headers=headers)

    assert response.status_code == 500
