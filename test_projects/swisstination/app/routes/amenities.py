from http import HTTPStatus

from flask import Blueprint, Response, request

from app.helpers import response_wrapper
from app.mongo import MongoCollections, get_client

amenities: Blueprint = Blueprint("amenities", __name__)


@amenities.route("/amenities/<string:object_id>", methods=["GET"])
def get_amenity_by_id(object_id: str) -> Response:
    """
    Fetches a specific amenity by its id

    :param object_id: integer id of amenity
    :return: Response
    """
    amenity_client = get_client(MongoCollections.AMENITIES)

    if not (amenity := amenity_client.find_one({"id": object_id})):
        return response_wrapper(
            code=HTTPStatus.NOT_FOUND,
            body={"error": f"No amenity found with id {object_id}"},
        )

    return response_wrapper(
        code=HTTPStatus.OK,
        body={"result": amenity},
    )


@amenities.route("/amenities/labels", methods=["GET"])
def list_amenity_labels() -> Response:
    """
    Fetches all unique amenities from the osm amenities

    Query parameters:
    - sort: asc or desc
    - max: maximum number of results

    :return: Response
    """
    order = request.args.get("sort", "desc").lower()
    limit = request.args.get("limit", "20")
    search = request.args.get("search", "")

    if order not in {"asc", "desc"}:
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={"error": "Invalid sort order"},
        )

    if not limit.isdigit() or int(limit) not in range(1, 101):
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={"error": "Invalid limit value"},
        )

    amenity_client = get_client(MongoCollections.AMENITIES)

    amenities = amenity_client.distinct(
        "amenity", {"amenity": {"$regex": search, "$options": "i"}}
    )
    amenities = [amenity.lower() for amenity in amenities]
    amenities.sort(reverse=order == "desc")

    max_results = min(int(limit), len(amenities))

    return response_wrapper(
        code=HTTPStatus.OK,
        body={"result": amenities[:max_results]},
    )
