from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from . import JWToken

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(data: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return JWToken.verify_token(data, credentials_exception)


oauth2_scheme2 = OAuth2PasswordBearer(tokenUrl="visitor/login")


def get_current_visitor(data: str = Depends(oauth2_scheme2)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return JWToken.verify_token(data, credentials_exception)