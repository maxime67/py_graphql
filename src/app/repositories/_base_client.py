import httpx
from app.core.config import settings
from app.core.exceptions import DALException

class BaseClient:
    """Client de base pour gérer les appels HTTP et les erreurs."""

    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)

    async def _request(self, method: str, url: str, **kwargs) -> httpx.Response:
        """Effectue une requête et gère les exceptions communes."""
        try:
            response = await self.client.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            # Erreur HTTP (4xx, 5xx)
            dal_exception = DALException(
                message=f"Erreur API: {e.response.status_code} pour {e.request.url}. Réponse: {e.response.text}",
                original_exception=e
            )
            dal_exception.status_code = e.response.status_code
            raise dal_exception from e
        except httpx.RequestError as e:
            # Erreur réseau (timeout, connexion impossible...)
            raise DALException(
                message=f"Erreur réseau pour {e.request.url}",
                original_exception=e
            ) from e

api_client = BaseClient(base_url=settings.MOVIE_API_BASE_URL)

