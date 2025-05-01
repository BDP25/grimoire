import argparse
import json
import logging
import sys

from bson import ObjectId
from pymongo import MongoClient


def main() -> None:
    """
    Ingests JSON data into MongoDB.
    """
    parser = argparse.ArgumentParser(
        description="Ingestion script for OSM data into MongoDB"
    )
    parser.add_argument(
        "file",
        type=argparse.FileType("r"),
        help="JSON file to ingest",
    )
    parser.add_argument(
        "--uri",
        type=str,
        help="URI for MongoDB",
        default="mongodb://localhost:27017/",
    )
    parser.add_argument(
        "--db",
        type=str,
        help="Database name",
        default="osm",
    )
    parser.add_argument(
        "--collection",
        type=str,
        help="Collection name",
        default="amenities",
    )
    parser.add_argument(
        "--drop",
        action="store_true",
        help="Drop collection before inserting data",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        help="Batch size",
        default=1000,
    )

    args = parser.parse_args()

    client: MongoClient = MongoClient(args.uri)
    db = client[args.db]
    collection = db[args.collection]

    data = json.load(args.file)

    if isinstance(data, list):
        logging.error("Expected a single json object")
        sys.exit(1)
    if "nodes" not in data:
        logging.error("Expected 'nodes' key in JSON object")
        sys.exit(1)
    if not isinstance(data["nodes"], list):
        logging.error("Expected 'nodes' key to be a list")
        sys.exit(1)
    if len(data["nodes"]) == 0:
        logging.error("Expected 'nodes' key to have at least one element")
        sys.exit(1)

    try:
        if args.drop:
            collection.drop()

        for i in range(0, len(data["nodes"]), args.batch_size):
            batch_data = data["nodes"][i : i + args.batch_size]

            # Transform ObjectIds
            trans_data = []
            for doc in batch_data:
                doc = convert_object_id(doc)
                trans_data.append(doc)

            collection.insert_many(trans_data)
    except Exception as e:
        logging.error("Failed to ingest data: %s", e)
        sys.exit(1)


def convert_object_id(doc: dict) -> dict:
    """
    Converts $oid to ObjectId.
    """
    for prop in doc:
        if isinstance(doc[prop], dict) and "$oid" in doc[prop]:
            doc[prop] = ObjectId(doc[prop]["$oid"])
    return doc


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )
    main()
