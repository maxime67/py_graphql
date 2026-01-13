from pydantic import BaseModel
from typing import List, Optional

from app.models.genre import Genre
from app.models.opinion import Opinion
from app.models.person import Person


class Movie(BaseModel):
    id: int
    title: str
    year: int
    duration: Optional[int] = None
    synopsis: Optional[str] = None
    genre: Genre
    director: Person
    actors: List[Person]
    opinions: List[Opinion]

