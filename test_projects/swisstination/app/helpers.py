import json
from collections.abc import Callable
from functools import wraps
from http import HTTPStatus
from typing import Any

import bcrypt
from flask import Response, session
from pydantic import SecretStr

from app.exceptions import AuthenticationError
from app.models.users import UserSession


def response_wrapper(
    code: HTTPStatus, body: dict | None = None, headers: dict | None = None
) -> Response:
    """
    Wraps the response in a clean and consistent way.

    :param code: HTTPStatus
    :param body: dict
    :param headers: dict
    """
    if body:
        response = Response(
            response=json.dumps(body, default=str),
            status=code,
            mimetype="application/json",
        )
    else:
        response = Response(
            response=None,
            status=code,
            mimetype="application/json",
        )

    if headers:
        for key, value in headers.items():
            response.headers[key] = value
    return response


def set_session(user: UserSession) -> None:
    """
    Sets the session cookie.

    :param user: pydantic user abstraction model
    """
    session["id"] = user.id
    session["is_authenticated"] = True
    session.permanent = True


def user_is_authenticated(f: Callable) -> Callable:
    """
    Checks if user has session cookie.

    :param f: function
    """

    @wraps(f)
    def func(*args: tuple, **kwargs: Any) -> Response | Callable:
        if not session.get("is_authenticated"):
            raise AuthenticationError("User is not authenticated.")
        return f(*args, **kwargs)

    return func


def hash_password(password: SecretStr) -> str:
    """
    Hashes the password.

    :param password: str
    """
    salt: bytes = b"$2b$12$3kPXS3K7eJN3.tSane82Oe"
    return bcrypt.hashpw(password.get_secret_value().encode(), salt).decode("utf-8")
