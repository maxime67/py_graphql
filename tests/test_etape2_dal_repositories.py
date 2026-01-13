"""
Tests de validation pour l'Étape 2 : Couche d'accès aux données (Repositories)

[Version Corrigée]
Cette version corrige les assertions pour accepter les arguments positionnels (args)
au lieu de forcer les arguments mots-clés (kwargs) lors de l'appel à _request.
Elle corrige également la simulation de DALException pour qu'elle corresponde
à la logique de _base_client.py.
"""

import pytest
import pytest_asyncio
from unittest.mock import MagicMock, AsyncMock
from app.core.exceptions import DALException
from app.models.movie import Movie
from app.models.genre import Genre

# --- Fixtures de données (simule les réponses de l'API) ---

@pytest.fixture
def mock_movie_data():
    """Données JSON brutes pour un film, simulées depuis l'API."""
    return {
        "id": 1,
        "title": "Inception",
        "year": 2010,
        "duration": 148,
        "synopsis": "Un voleur...",
        "genre": {"id": 1, "label": "Science-Fiction"},
        "director": {"id": 1, "last_name": "Nolan", "first_name": "Christopher"},
        "actors": [{"id": 2, "last_name": "DiCaprio", "first_name": "Leonardo"}],
        "opinions": []
    }

@pytest.fixture
def mock_genre_list_data():
    """Données JSON brutes pour une liste de genres."""
    return [
        {"id": 1, "label": "Science-Fiction"},
        {"id": 2, "label": "Drame"}
    ]

# --- Tests ---

@pytest.mark.asyncio
async def test_movie_repo_find_by_id_success(mocker, mock_movie_data):
    """
    Vérifie que movie_repository.find_by_id retourne un objet Movie
    en cas de succès.
    """
    # 1. Mock de l'api_client
    mock_response = MagicMock()
    mock_response.json.return_value = mock_movie_data
    mock_api_client = AsyncMock()
    mock_api_client._request.return_value = mock_response

    # On "patch" l'instance importée dans le module du repository
    mocker.patch('app.repositories.movie_repository.api_client', mock_api_client)

    # 2. Appel de la méthode à tester
    from app.repositories.movie_repository import movie_repository
    movie = await movie_repository.find_by_id(1)

    # 3. Assertions
    mock_api_client._request.assert_called_once_with("GET", "/movies/1")
    assert movie is not None
    assert isinstance(movie, Movie)
    assert movie.title == "Inception"

@pytest.mark.asyncio
async def test_movie_repo_find_by_id_not_found(mocker):
    """
    Vérifie que movie_repository.find_by_id retourne None si l'API
    lève une DALException avec un status 404.
    """
    # 1. Mock de l'api_client pour qu'il lève une erreur 404
    mock_api_client = AsyncMock()

    # 1. Crée l'exception
    mock_exception = DALException("Not Found")
    # 2. Attache le status_code
    mock_exception.status_code = 404
    # 3. La définit comme side_effect
    mock_api_client._request.side_effect = mock_exception

    mocker.patch('app.repositories.movie_repository.api_client', mock_api_client)

    # 2. Appel de la méthode à tester
    from app.repositories.movie_repository import movie_repository
    movie = await movie_repository.find_by_id(999)

    # 3. Assertions
    mock_api_client._request.assert_called_once_with("GET", "/movies/999")
    assert movie is None

@pytest.mark.asyncio
async def test_movie_repo_list(mocker, mock_movie_data):
    """
    Vérifie que movie_repository.list retourne une liste de Movies
    et passe correctement les paramètres skip/limit.
    """
    # 1. Mock de l'api_client
    mock_response = MagicMock()
    mock_response.json.return_value = [mock_movie_data] # L'API retourne une liste
    mock_api_client = AsyncMock()
    mock_api_client._request.return_value = mock_response
    mocker.patch('app.repositories.movie_repository.api_client', mock_api_client)

    # 2. Appel de la méthode à tester
    from app.repositories.movie_repository import movie_repository
    movies = await movie_repository.list(skip=5, limit=10)

    # 3. Assertions
    expected_params = {"skip": 5, "limit": 10}
    mock_api_client._request.assert_called_once_with("GET", "/movies/", params=expected_params)
    assert isinstance(movies, list)
    assert isinstance(movies[0], Movie)
    assert movies[0].id == 1

@pytest.mark.asyncio
async def test_genre_repo_list(mocker, mock_genre_list_data):
    """
    Vérifie que genre_repository.list retourne une liste de Genres.
    """
    # 1. Mock de l'api_client
    mock_response = MagicMock()
    mock_response.json.return_value = mock_genre_list_data
    mock_api_client = AsyncMock()
    mock_api_client._request.return_value = mock_response
    mocker.patch('app.repositories.genre_repository.api_client', mock_api_client)

    # 2. Appel de la méthode à tester
    from app.repositories.genre_repository import genre_repository
    genres = await genre_repository.list()

    # 3. Assertions
    mock_api_client._request.assert_called_once_with("GET", "/genres/")
    assert isinstance(genres, list)
    assert isinstance(genres[0], Genre)
    assert genres[0].label == "Science-Fiction"