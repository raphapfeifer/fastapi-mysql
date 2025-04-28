from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import app.routers.routers_login as login


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/login/")


def token_verifier(token=Depends(oauth_scheme)):
    login.verify_token(access_token=token)