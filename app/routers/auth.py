import os
import requests
from fastapi import HTTPException, Header

def verify_authorization(token: str = Header(None)):
    """
        The function is to be called before the controlers.
        It reads the token in the header and verify it with the APi Authentication
    """
    if token is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    url = os.getenv("AUTHURL")
    key = os.getenv("SERVICEKEY")
    payload = {"token":token,"service_key":key}
    response = requests.post(f"http://{url}/authentification/validation_token",
                             json=payload, timeout=10)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code,
                            detail="Failed to send data to external API")
    validation = response.json().get("validation")
    if validation is None or validation is not True:
        raise HTTPException(status_code=403, detail="UnAuthorized")
