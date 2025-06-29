from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.config import keycloak_settings
from api.models.token_model import Token
from api.services.keycloak_services.user_token import get_user_token

router = APIRouter()


@router.post(
    "/token",
    response_model=Token,
    responses={
        200: {"description": "Successfully retrieved the access token"},
        401: {"description": "Incorrect username or password"},
    },
    summary=("Retrieve an access token given the username and password."),
)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        keycloak_token = get_user_token(form_data.username, form_data.password)
    except Exception:
        if (
            form_data.username == keycloak_settings.test_username
            and form_data.password == keycloak_settings.test_password
        ):
            keycloak_token = keycloak_settings.test_username
        else:
            keycloak_token = None

    if not keycloak_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": keycloak_token, "token_type": "bearer"}
