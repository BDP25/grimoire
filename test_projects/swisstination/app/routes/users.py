import base64
from datetime import datetime
from http import HTTPStatus

from bson import ObjectId
from flask import Blueprint, Response, request, session
from pydantic import SecretStr

from app.helpers import (
    hash_password,
    response_wrapper,
    set_session,
    user_is_authenticated,
)
from app.models.users import (
    UserLogin,
    UserProfileRead,
    UserProfileWrite,
    UserSession,
    UserSignup,
)
from app.mongo import MongoCollections, get_client

users: Blueprint = Blueprint("users", __name__)


@users.route("/users/signup", methods=["POST"])
def signup() -> Response:
    """
    Creates a new user.

    :return: Response
    """
    user_client = get_client(MongoCollections.USERS)
    data = request.get_json()
    date = datetime.now().strftime("%Y-%m-%d")

    try:
        user = UserSignup(**data, date_joined=date)
        user.email = user.email.lower()

        if user_client.find_one(
            {
                "$or": [
                    {"email": user.email},
                    {"username": {"$regex": f"^{user.username}$", "$options": "i"}},
                ]
            }
        ):
            return response_wrapper(
                code=HTTPStatus.CONFLICT,
                body={"error": "User already exists"},
            )

        user.password = SecretStr(hash_password(user.password))

    except ValueError as e:
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={"error": str(e)},
        )

    result = user_client.insert_one(user.model_dump())
    user_session = UserSession(**user.model_dump(), _id=str(result.inserted_id))
    set_session(user_session)
    return response_wrapper(code=HTTPStatus.CREATED)


@users.route("/users/login", methods=["POST"])
def login() -> Response:
    """
    Logs in a user.

    :return: Response
    """
    user_client = get_client(MongoCollections.USERS)
    data = request.get_json()

    try:
        user = UserLogin(**data)
        user_data = user_client.find_one({"email": user.email})

        password = hash_password(user.password)

        if not user_data or user_data["password"] != password:
            return response_wrapper(
                code=HTTPStatus.UNAUTHORIZED,
                body={"error": "Invalid email or password"},
            )

        user_id = user_data.pop("_id")
        user_session = UserSession(**user_data, _id=str(user_id))
        set_session(user_session)
    except ValueError as e:
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={"error": str(e)},
        )

    return response_wrapper(code=HTTPStatus.OK)


@users.route("/users/logout", methods=["POST"])
def logout() -> Response:
    """
    Logs out a user.

    :return: Response
    """
    session.clear()
    return response_wrapper(
        code=HTTPStatus.OK,
        body={"message": "Logged out successfully"},
    )


@users.route("/users/<string:_id>", methods=["GET"])
def get_user_by_id(_id: str) -> Response:
    """
    Fetches a specific user by their username

    :param _id: string id of user
    :return: Response
    """
    user_client = get_client(MongoCollections.USERS)

    if not (user := user_client.find_one({"_id": ObjectId(_id)})):
        return response_wrapper(
            code=HTTPStatus.NOT_FOUND,
            body={"error": f"No user found with id {_id}"},
        )

    return response_wrapper(
        code=HTTPStatus.OK,
        body={"result": UserProfileRead(**user).model_dump()},
    )


@users.route("/users/me", methods=["GET"])
@user_is_authenticated
def get_current_user() -> Response:
    """
    Fetches the current user

    :return: Response
    """
    user_client = get_client(MongoCollections.USERS)

    if not (user := user_client.find_one({"_id": ObjectId(session.get("id"))})):
        return response_wrapper(
            code=HTTPStatus.NOT_FOUND,
            body={"error": "No user found"},
        )

    return response_wrapper(
        code=HTTPStatus.OK,
        body={"result": UserProfileRead(**user).model_dump()},
    )


@users.route("/users/me", methods=["PATCH"])
@user_is_authenticated
def update_current_user() -> Response:
    """
    Updates the current user

    :return: Response
    """
    user_client = get_client(MongoCollections.USERS)
    data = request.get_json()

    try:
        user = UserProfileWrite(**data)
    except ValueError as e:
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={"error": str(e)},
        )

    user_client.update_one(
        {"email": session.get("email")},
        {"$set": user.model_dump(exclude_unset=True)},
    )
    return response_wrapper(
        code=HTTPStatus.OK,
        body={"message": "User updated successfully"},
    )


@users.route("/users/me/avatar", methods=["POST"])
@user_is_authenticated
def update_avatar() -> Response:
    """
    Updates the current user's avatar

    :return: Response
    """
    user_client = get_client(MongoCollections.USERS)

    if not (avatar := request.files.get("avatar")):
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={"error": "No file part"},
        )
    if not avatar.content_type.startswith("image/"):
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={"error": "File must be an image"},
        )

    user_client.update_one(
        {"email": session.get("email")},
        {"$set": {"avatar": avatar.read(), "avatar_type": avatar.content_type}},
    )
    return response_wrapper(
        code=HTTPStatus.OK,
        body={"message": "Avatar updated successfully"},
    )


@users.route("/users/<string:username>/avatar", methods=["GET"])
def get_avatar(username: str) -> Response:
    """
    Fetches a specific user's avatar by their username

    :param username: string username of user
    :return: Response
    """
    user_client = get_client(MongoCollections.USERS)

    if not (
        user := user_client.find_one(
            {"username": {"$regex": f"^{username}$", "$options": "i"}}
        )
    ):
        return response_wrapper(
            code=HTTPStatus.NOT_FOUND,
            body={"error": f"No user found with username {username}"},
        )

    if not user.get("avatar"):
        return response_wrapper(
            code=HTTPStatus.NOT_FOUND,
            body={"error": "No avatar found for this user"},
        )

    data = base64.b64decode(user["avatar"])

    return Response(
        data,
        mimetype=user["avatar_type"],
    )
