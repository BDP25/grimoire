import os
from enum import Enum

import pymongo
from pymongo.collection import Collection

MONGO_DB = os.getenv("MONGO_DB", "swisstination")


class MongoCollections(Enum):
    AMENITIES = os.getenv("MONGO_COLLECTIONS_AMENITIES", "amenities")
    TOURS = os.getenv("MONGO_COLLECTIONS_TOURS", "tours")
    USERS = os.getenv("MONGO_COLLECTIONS_USERS", "users")


def get_client(collection: MongoCollections) -> Collection:
    return pymongo.MongoClient(
        host=os.getenv("MONGO_HOST", "localhost"),
        port=int(os.getenv("MONGO_PORT", "27017")),
        maxPoolSize=100,
        waitQueueTimeoutMS=2000,
    )[MONGO_DB][collection.value]
