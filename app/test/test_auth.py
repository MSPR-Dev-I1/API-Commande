from fastapi import HTTPException
import pytest
from app.routers.auth import verify_authorization

def test_verify_authorization_no_header():
    """Test when authorization header is missing"""
    with pytest.raises(HTTPException) as exc_info:
        verify_authorization(None)
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Authorization header missing"

def test_verify_authorization_invalid_token(mocker):
    """Test when the token is invalid"""
    mocker.patch("app.routers.auth.os.getenv",
                 side_effect=lambda k: "http://fake-url" if k == "AUTHURL" else "fake-key")
    mock_response = mocker.patch("app.routers.auth.requests.post")
    mock_response.return_value.status_code = 401
    mock_response.return_value.json.return_value = {"validation": False}

    with pytest.raises(HTTPException) as exc_info:
        verify_authorization("invalid-token")
    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Failed to send data to external API"

def test_verify_authorization_unauthorized(mocker):
    """Test when the token is unauthorized"""
    mocker.patch("app.routers.auth.os.getenv",
                 side_effect=lambda k: "http://fake-url" if k == "AUTHURL" else "fake-key")
    mock_response = mocker.patch("app.routers.auth.requests.post")
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = {"validation": False}

    with pytest.raises(HTTPException) as exc_info:
        verify_authorization("unauthorized-token")
    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "UnAuthorized"

def test_verify_authorization_success(mocker):
    """Test when the token is valid"""
    mocker.patch("app.routers.auth.os.getenv",
                 side_effect=lambda k: "http://fake-url" if k == "AUTHURL" else "fake-key")
    mock_response = mocker.patch("app.routers.auth.requests.post")
    mock_response.return_value.status_code = 200
    mock_response.return_value.json.return_value = {"validation": True}

    try:
        verify_authorization("valid-token")
    except HTTPException:
        pytest.fail("verify_authorization raised HTTPException unexpectedly!")
