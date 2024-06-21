import uuid
from typing import Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    favorite_anime: str = Field(...)

    class Config:
        populate_by_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "NicK",
                "favorite_anime": "Fullmetal Alchemist"
            }
        }

class UserUpdate(BaseModel):
    name: Optional[str]
    favorite_anime: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "name": "NicK",
                "favorite_anime": "Fullmetal Alchemist"
            }
        }