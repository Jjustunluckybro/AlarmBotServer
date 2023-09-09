import os
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

security = HTTPBasic()


def authenticate_client(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    username = os.getenv("CLIENT_NAME")
    password = os.getenv("CLIENT_PASSWORD")

    if credentials.username != username or credentials.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'User {credentials.username} not found',
            headers={'WWW-Authenticate': 'Basic'}
        )
    return True
