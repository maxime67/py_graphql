from typing import List, Optional
import httpx
from app.core.exceptions import DALException
from app.models.movie import Movie
from app.repositories._base_client import api_client


class MovieRepository:

    async def list(self, skip: int = 0, limit: int = 100) -> List[Movie]:
        response = await api_client._request("GET", "/movies/", params={"skip": skip, "limit": limit})
        return [Movie.model_validate(m) for m in response.json()]

    async def find_by_id(self, movie_id: int) -> Optional[Movie]:
        try:
            response = await api_client._request("GET", f"/movies/{movie_id}")
            return Movie.model_validate(response.json())
        except DALException as e:
            if e.status_code == 404:
                return None
            raise
movie_repository = MovieRepository()