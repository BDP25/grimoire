from bson import ObjectId
from pydantic import BaseModel, Field


class Destination(BaseModel):
    amenityId: str
    title: str
    description: str


class NewTour(BaseModel):
    title: str
    description: str
    duration: int
    likes: int = 0
    creatorId: ObjectId = Field()
    tags: list[str]
    destinations: list[Destination]

    class Config:
        arbitrary_types_allowed = True
