import os
from datetime import timedelta
from http import HTTPStatus

from flask import Flask, Response
from flask_cors import CORS
from pymongo.errors import ConnectionFailure

from app.exceptions import AuthenticationError
from app.helpers import response_wrapper
from app.routes.amenities import amenities
from app.routes.tours import tours
from app.routes.users import users

app = Flask(
    __name__,
    static_url_path="/",
    static_folder="static",
    template_folder="templates",
)

app.secret_key = os.getenv("SECRET_KEY", "very-secret-key")
app.permanent_session_lifetime = timedelta(days=7)

app.register_blueprint(amenities, url_prefix="/api/v1")
app.register_blueprint(tours, url_prefix="/api/v1")
app.register_blueprint(users, url_prefix="/api/v1")

# Allow cors origin source: https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
cors = CORS(app, supports_credentials=True)


@app.errorhandler(ConnectionFailure)
def handle_connection_error(error: ConnectionFailure) -> Response:
    app.logger.warning(error)
    return response_wrapper(
        code=HTTPStatus.INTERNAL_SERVER_ERROR,
        body={"error": "Connection pool is empty. Try again later."},
    )


@app.errorhandler(AuthenticationError)
def handle_authentication_error(error: AuthenticationError) -> Response:
    app.logger.info(error)
    return response_wrapper(
        code=HTTPStatus.UNAUTHORIZED,
        body={"error": error.message},
    )
