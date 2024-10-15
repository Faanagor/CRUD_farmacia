from fastapi_jwt_auth import AuthJWT
from fastapi import Depends
from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = "supersecretkey"


@AuthJWT.load_config
def get_config():
    return Settings()


def get_current_user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return current_user
