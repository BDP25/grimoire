from http import HTTPStatus

import mongomock
import pytest
from pydantic import SecretStr

from app.helpers import hash_password
from app.mongo import MongoCollections, get_client

# api/v1/users/signup


@mongomock.patch(servers=(("localhost", 27017),))
def test_signup_user_success(client) -> None:
    response = client.post(
        "api/v1/users/signup",
        json={
            "username": "test_user",
            "password": "test_password",
            "email": "user@blabla.com",
        },
    )
    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.parametrize(
    "payload",
    [
        {"username": "test_user", "password": "test_password"},
        {"username": "test_user", "email": "user@blabla.com"},
        {"password": "test_password", "email": "user@blabla.com"},
    ],
)
@mongomock.patch(servers=(("localhost", 27017),))
def test_signup_user_missing_parameter_error(client, payload) -> None:
    response = client.post("api/v1/users/signup", json=payload)
    assert response.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.parametrize(
    "payload",
    [
        {
            "username": "test_user",
            "password": "test_password",
            "email": "other@blabla.com",
        },
        {
            "username": "other_user",
            "password": "other_password",
            "email": "user@blabla.com",
        },
        {
            "username": "TEST_user",
            "password": "test_password",
            "email": "other@blabla.com",
        },
        {
            "username": "test_user",
            "password": "test_password",
            "email": "USER@blabla.com",
        },
    ],
)
@mongomock.patch(servers=(("localhost", 27017),))
def test_signup_user_duplicate_error(client, payload) -> None:
    client.post(
        "api/v1/users/signup",
        json={
            "username": "test_user",
            "password": "test_password",
            "email": "user@blabla.com",
        },
    )
    response = client.post("api/v1/users/signup", json=payload)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json["error"] == "User already exists"


# api/v1/users/login


@mongomock.patch(servers=(("localhost", 27017),))
def test_login_user_success(client) -> None:
    users_client = get_client(MongoCollections.USERS)
    users_client.insert_one(
        {
            "username": "test_user",
            "password": hash_password(SecretStr("test_password")),
            "email": "user@blabla.com",
        }
    )

    response = client.post(
        "api/v1/users/login",
        json={"email": "user@blabla.com", "password": "test_password"},
    )
    assert response.status_code == HTTPStatus.OK


@mongomock.patch(servers=(("localhost", 27017),))
def test_login_user_not_found(client) -> None:
    response = client.post(
        "api/v1/users/login",
        json={"email": "dora@blabla.com", "password": "test_password"},
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json["error"] == "Invalid email or password"


# api/v1/users/logout


@mongomock.patch(servers=(("localhost", 27017),))
def test_logout_user_success(client) -> None:
    client.post(
        "api/v1/users/signup",
        json={
            "username": "test_user",
            "password": "test_password",
            "email": "user@blabla.com",
        },
    )
    response = client.post("api/v1/users/logout")
    assert response.status_code == HTTPStatus.OK


# api/v1/users/<username>
