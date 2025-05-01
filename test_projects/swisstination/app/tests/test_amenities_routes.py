from http import HTTPStatus

import mongomock
import pytest

# api/v1/amenities


@mongomock.patch(servers=(("localhost", 27017),))
@pytest.mark.parametrize(
    "object_id, output_keys",
    [
        ("1", ["_id", "id", "amenity", "name", "lat", "lon"]),
        ("2", ["_id", "id", "amenity", "name", "lat", "lon"]),
        ("3", ["_id", "id", "amenity", "name", "lat", "lon"]),
    ],
)
def test_get_amenity_by_id_success(
    client, create_amenities, object_id, output_keys
) -> None:
    create_amenities()
    response = client.get(f"api/v1/amenities/{object_id}")
    assert response.status_code == HTTPStatus.OK
    assert all(key in response.json["result"] for key in output_keys)


@mongomock.patch(servers=(("localhost", 27017),))
def test_get_amenity_by_id_not_found(client, create_amenities) -> None:
    create_amenities()
    response = client.get("api/v1/amenities/999")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json == {"error": "No amenity found with id 999"}


# api/v1/amenities/labels


@mongomock.patch(servers=(("localhost", 27017),))
def test_get_amenity_labels_success(client, create_amenities) -> None:
    create_amenities()
    response = client.get("api/v1/amenities/labels")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json["result"]) == 3


@mongomock.patch(servers=(("localhost", 27017),))
def test_get_amenity_labels_max_success(client, create_amenities) -> None:
    create_amenities()
    response = client.get("api/v1/amenities/labels?limit=2")
    assert response.status_code == HTTPStatus.OK
    assert len(response.json["result"]) == 2


@mongomock.patch(servers=(("localhost", 27017),))
@pytest.mark.parametrize(
    "sort_order, expected_label",
    [
        ("asc", "bench"),
        ("desc", "restaurant"),
    ],
)
def test_get_amenity_labels_sort_success(
    client, create_amenities, sort_order, expected_label
) -> None:
    create_amenities()
    response = client.get(f"api/v1/amenities/labels?sort={sort_order}")
    assert response.status_code == HTTPStatus.OK
    assert response.json["result"][0] == expected_label
