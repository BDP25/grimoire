import pytest

from app.main import app
from app.mongo import MongoCollections, get_client


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


@pytest.fixture
def create_amenities():
    def _create_amenities():
        amenities_client = get_client(MongoCollections.AMENITIES)
        amenities_client.insert_many(
            [
                {
                    "id": "1",
                    "amenity": "bench",
                    "name": "Bench A",
                    "lat": "47.378177",
                    "lon": "8.540192",
                },
                {
                    "id": "2",
                    "amenity": "fountain",
                    "name": "Fountain Geneve",
                    "lat": "47.37174",
                    "lon": "8.53466",
                },
                {
                    "id": "3",
                    "amenity": "restaurant",
                    "name": "Brauerei Baar",
                    "lat": "47.678177",
                    "lon": "8.140192",
                },
                {
                    "id": "4",
                    "amenity": "bench",
                    "name": "Bench B",
                    "lat": "47.378134",
                    "lon": "8.540112",
                },
            ]
        )

    return _create_amenities
