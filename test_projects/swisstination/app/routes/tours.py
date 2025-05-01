from http import HTTPStatus

import pymongo
from bson import ObjectId
from flask import Blueprint, Response, request, session

from app.helpers import response_wrapper, user_is_authenticated
from app.models.tours import NewTour
from app.mongo import MongoCollections, get_client

tours: Blueprint = Blueprint("tours", __name__)


@tours.route("/tours", methods=["GET"])
def list_tours() -> Response:
    """
    Fetches all tours from mongodb

    Query parameters:
    - sort: Sort field (likes, duration, title)
    - order: Sort order (asc, desc)
    - tags: Filter by tags (comma separated)
    - search: Search text in title and description

    :return: Response
    """
    sort_field = request.args.get("sort", "likes")
    sort_order = request.args.get("order", "desc").lower()
    tags_filter = request.args.get("tags", "")
    search_text = request.args.get("search", "")

    if sort_field not in {"likes", "duration", "title"}:
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={"error": "Invalid sort field use one of likes, duration, title"},
        )

    if sort_order not in {"asc", "desc"}:
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={"error": "Invalid sort order use one of asc, desc"},
        )

    tour_client = get_client(MongoCollections.TOURS)

    direction = pymongo.ASCENDING if sort_order == "asc" else pymongo.DESCENDING

    query_filter: dict = {}
    if tags_filter:
        tags = [tag.strip().lower() for tag in tags_filter.split(",")]
        query_filter["tags"] = {"$in": tags}
    if search_text:
        query_filter["$or"] = [
            {"title": {"$regex": search_text, "$options": "i"}},
            {"description": {"$regex": search_text, "$options": "i"}},
        ]

    tours = list(
        tour_client.find(
            query_filter,
            {
                "id": 1,
                "title": 1,
                "description": 1,
                "duration": 1,
                "likes": 1,
                "creatorId": 1,
                "tags": 1,
                "_id": 1,
            },
        ).sort(sort_field, direction)
    )

    return response_wrapper(
        code=HTTPStatus.OK,
        body={"result": tours},
        headers={"X-Total-Count": len(tours)},
    )


@tours.route("/tours", methods=["POST"])
@user_is_authenticated
def create_tour() -> Response:
    """
    Creates a new tour.

    :return: Response
    """
    tour_client = get_client(MongoCollections.TOURS)
    data = request.get_json()

    if not (user_id := session.get("id")):
        return response_wrapper(
            code=HTTPStatus.INTERNAL_SERVER_ERROR,
            body={"error": "Could not retrieve user session, please login again"},
        )

    try:
        tour = NewTour(**data, creatorId=ObjectId(user_id))
        tour.likes = 0
        result = tour_client.insert_one(tour.model_dump())
    except ValueError as e:
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={"error": str(e)},
        )

    return response_wrapper(
        code=HTTPStatus.CREATED,
        body={"message": "Tour created successfully", "id": str(result.inserted_id)},
    )


@tours.route("/tours/<string:object_id>", methods=["GET"])
def get_tour_by_id(object_id: str) -> Response:
    """
    Fetches a specific tour by its id.

    :param object_id: string id of the tour
    :return: Response
    """
    tour_client = get_client(MongoCollections.TOURS)
    amenity_client = get_client(MongoCollections.AMENITIES)

    try:
        _id = ObjectId(object_id)
    except Exception:
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={"error": "Invalid ObjectId format"},
        )

    if not (tour := tour_client.find_one({"_id": _id})):
        return response_wrapper(
            code=HTTPStatus.NOT_FOUND,
            body={"error": f"No tour found with id {_id}"},
        )

    for dest in tour["destination"]:
        dest["amenity"] = amenity_client.find_one({"id": dest["amenityId"]})

    return response_wrapper(
        code=HTTPStatus.OK,
        body={"result": tour},
    )


@tours.route("/tours/tags", methods=["GET"])
def list_tags() -> Response:
    """
    Fetches all unique tags from all tours

    :return: Response
    """
    tour_client = get_client(MongoCollections.TOURS)

    tags = tour_client.distinct("tags")
    tags = [tag.lower() for tag in tags]

    return response_wrapper(
        code=HTTPStatus.OK,
        body={"result": tags},
        headers={"X-Total-Count": len(tags)},
    )


@tours.route("/tours/<string:object_id>/like", methods=["POST", "DELETE"])
@user_is_authenticated
def vote_tour(object_id: str) -> Response:
    """
    Likes/Unlikes a specific tour by its id.

    :param object_id: string id of the tour
    :return: Response
    """
    tour_client = get_client(MongoCollections.TOURS)
    user_client = get_client(MongoCollections.USERS)

    try:
        _id = ObjectId(object_id)
    except Exception:
        return response_wrapper(
            code=HTTPStatus.BAD_REQUEST,
            body={"error": "Invalid ObjectId format"},
        )

    user_id = session.get("id")
    if not (user_data := user_client.find_one({"_id": ObjectId(user_id)})):
        return response_wrapper(
            code=HTTPStatus.INTERNAL_SERVER_ERROR,
            body={"error": "Could not retrieve user session, please login again"},
        )

    if not (tour := tour_client.find_one({"_id": _id})):
        return response_wrapper(
            code=HTTPStatus.NOT_FOUND,
            body={"error": f"No tour found with id {_id}"},
        )

    if request.method == "POST":
        if _id in user_data.get("likedTours", []):
            return response_wrapper(
                code=HTTPStatus.BAD_REQUEST,
                body={"error": "You have already liked this tour"},
            )

        tour_client.update_one({"_id": _id}, {"$inc": {"likes": 1}})
        new_likes = tour.get("likes", 0) + 1

        user_client.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$push": {"likedTours": _id},
                "$pull": {"dislikedTours": _id},
            },
        )

    else:
        if _id in user_data.get("dislikedTours", []):
            return response_wrapper(
                code=HTTPStatus.BAD_REQUEST,
                body={"error": "You have already disliked this tour"},
            )

        tour_client.update_one({"_id": _id}, {"$inc": {"likes": -1}})
        new_likes = tour.get("likes", 0) - 1

        user_client.update_one(
            {"_id": ObjectId(user_id)},
            {
                "$push": {"dislikedTours": _id},
                "$pull": {"likedTours": _id},
            },
        )

    return response_wrapper(
        code=HTTPStatus.OK,
        body={
            "result": {
                "message": "Vote successful",
                "id": str(object_id),
                "likes": new_likes,
            }
        },
    )
