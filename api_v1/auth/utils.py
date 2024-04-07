from datetime import datetime, timedelta

import bcrypt
import jwt

from core.config import settings


def encode_jwt(
    payload: dict,
    key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    encoded = jwt.encode(
        payload,
        key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithm=[algorithm],
    )
    return decoded


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")


def validate_password(
    password: str,
    hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=hashed_password.encode("utf-8"),
    )
