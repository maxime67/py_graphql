from typing import List

from app.models.genre import Genre
from app.repositories._base_client import api_client


class GenreRepository:
    async def list(self) -> List[Genre]:
        response = await api_client._request("GET", "/genres/")
        return [Genre.model_validate(g) for g in response.json()]


genre_repository = GenreRepository()