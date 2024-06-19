from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_connection_database(mocker):
    """
        Cas passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("app.models.Base.metadata.create_all", return_value=None)

    response = client.post("/database")

    assert response.status_code == 200
    assert response.json() == "database created"

def test_connection_database_error_500(mocker):
    """
        Cas non passant (erreur sur la connexion sur la base de données)
    """
    mocker.patch("app.models.Base.metadata.create_all", side_effect=Exception("Connection error"))

    response = client.post("/database")

    assert response.status_code == 500
