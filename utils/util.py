from abc import ABC, abstractmethod
import os
from datetime import datetime, timedelta
from typing import Union, Any, Dict
from passlib.context import CryptContext
from jose import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]  # should be kept secret
JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]  # should be kept secret

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_hashed_password(password: str, hashed_password: str) -> bool:
    return password_context.verify(password, hashed_password)


class Token(ABC):
    @staticmethod
    def _get_to_encode(
        subject: Union[str, Any], expires_delta: Union[timedelta, None] = None
    ) -> Dict:
        if expires_delta is not None:
            expires_delta = datetime.utcnow() + expires_delta  # type: ignore
        else:
            expires_delta = datetime.utcnow() + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )  # type: ignore

        return {"exp": expires_delta, "sub": str(subject)}

    @abstractmethod
    def create_token(
        self, subject: Union[str, Any], expires_delta: Union[timedelta, None] = None
    ):
        pass


class AccessToken(Token):
    def create_token(
        self, subject: Union[str, Any], expires_delta: Union[timedelta, None] = None
    ) -> str:
        to_encode = self._get_to_encode(subject, expires_delta)
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
        return encoded_jwt


class RefreshToken(Token):
    def create_token(
        self, subject: Union[str, Any], expires_delta: Union[timedelta, None] = None
    ) -> str:
        to_encode = self._get_to_encode(subject, expires_delta)
        encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
        return encoded_jwt
