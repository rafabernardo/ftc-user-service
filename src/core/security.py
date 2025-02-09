import hashlib

import jwt
from core.settings import settings
from fastapi import HTTPException
from schemas.token import Token


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def encode_jwt(token_data: dict) -> Token:
    encoded_token = jwt.encode(
        token_data,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_token


def decode_jwt(jwt_token: str) -> dict:
    # Decode JWT
    decoded_jwt = jwt.decode(
        jwt_token,
        settings.SECRET_KEY,
        algorithms=settings.ALGORITHM,
    )
    return decoded_jwt


def verify_jwt(token: str) -> dict:
    try:
        payload = decode_jwt(token)
        return payload
    except jwt.ExpiredSignatureError as err:
        raise HTTPException(status_code=401, detail="Token expired") from err
    except jwt.InvalidTokenError as err:
        raise HTTPException(status_code=401, detail="Invalid token") from err


def verify_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password
