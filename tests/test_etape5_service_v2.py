"""
Tests de validation pour l'Étape 5 : Service d'analyse avancé (Version 2 - Dynamique)

Objectif :
1. Vérifier que les fonctions `get_ai_...` appellent bien le LLM.
2. Vérifier que la fonction principale `analyze_movie` (V2)
   n'appelle QUE les fonctions nécessaires (en fonction des booléens).
3. Vérifier que les appels aux repositories sont corrects.

Prérequis :
- Les TODOs de `app/services/movie_analyzer_v2.py` sont complétés.
"""

import pytest
import strawberry
from unittest.mock import AsyncMock, MagicMock, patch
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.person import Person
from app.models.opinion import Opinion
from app.models.member import Member


# --- Fixtures ---

@pytest.fixture
def mock_llm():
    """Fixture pour un LLM mocké."""
    llm = MagicMock()
    # Simule la réponse de llm.ainvoke(...)
    mock_response = MagicMock()
    mock_response.content = "Réponse du LLM"
    llm.ainvoke = AsyncMock(return_value=mock_response)
    return llm


@pytest.fixture
def mock_movie():
    """Fixture pour un objet Movie Pydantic complet."""
    return Movie(
        id=1,
        title="Inception",
        year=2010,
        synopsis="Un voleur qui vole des secrets...",
        genre=Genre(id=1, label="Science-Fiction"),
        director=Person(id=1, last_name="Nolan", first_name="Christopher"),
        actors=[Person(id=2, last_name="DiCaprio", first_name="Leonardo")],
        opinions=[
            Opinion(id=1, note=5, comment="Génial!", movie_id=1, member=Member(id=1, login="user1"))
        ]
    )


@pytest.fixture
def mock_genres():
    """Fixture pour une liste d'objets Genre Pydantic."""
    return [
        Genre(id=1, label="Science-Fiction"),
        Genre(id=2, label="Drame")
    ]


# --- Tests des helpers LLM ---

@pytest.mark.asyncio
async def test_get_ai_summary(mock_llm):
    """Teste le prompt de résumé."""
    from app.services.movie_analyzer_v2 import get_ai_summary
    synopsis = "Un long synopsis..."
    result = await get_ai_summary(mock_llm, synopsis)

    assert result == "Réponse du LLM"
    mock_llm.ainvoke.assert_called_once()
    prompt_call = mock_llm.ainvoke.call_args[0][0]
    assert synopsis in prompt_call  # Vérifie que le synopsis est dans le prompt


@pytest.mark.asyncio
async def test_get_ai_summary_no_synopsis(mock_llm):
    """Teste que le LLM n'est pas appelé si le synopsis est vide."""
    from app.services.movie_analyzer_v2 import get_ai_summary
    result = await get_ai_summary(mock_llm, None)

    assert result is None
    mock_llm.ainvoke.assert_not_called()


# ... (Des tests similaires pourraient être écrits pour get_ai_opinion_summary,
# get_ai_best_genre, et get_ai_tags)

# --- Test du service principal (V2) ---

@pytest.mark.asyncio
async def test_service_v2_analyze_movie_partial_request(mocker, mock_llm, mock_movie):
    """
    Teste analyze_movie V2 avec une demande partielle (juste aiSummary).
    Vérifie que SEULS les appels nécessaires sont faits.
    """
    # 1. Mocker les dépendances (repositories)
    mock_movie_repo = AsyncMock()
    mock_movie_repo.find_by_id.return_value = mock_movie
    mocker.patch('app.services.movie_analyzer_v2.movie_repository', mock_movie_repo)

    mock_genre_repo = AsyncMock()
    mocker.patch('app.services.movie_analyzer_v2.genre_repository', mock_genre_repo)

    # 2. Mocker les helpers LLM (pour les espionner)
    mock_summary = AsyncMock(return_value="Résumé IA")
    mock_opinion = AsyncMock()
    mock_genre = AsyncMock()
    mock_tags = AsyncMock()

    mocker.patch('app.services.movie_analyzer_v2.get_ai_summary', mock_summary)
    mocker.patch('app.services.movie_analyzer_v2.get_ai_opinion_summary', mock_opinion)
    mocker.patch('app.services.movie_analyzer_v2.get_ai_best_genre', mock_genre)
    mocker.patch('app.services.movie_analyzer_v2.get_ai_tags', mock_tags)

    # 3. Appel du service
    from app.services.movie_analyzer_v2 import analyze_movie
    result = await analyze_movie(
        movie_id="1",
        ai_summary=True,
        ai_opinion_summary=False,
        ai_best_genre=False,
        ai_tags=False,
        llm=mock_llm
    )

    # 4. Assertions
    # Le repo de film a été appelé
    mock_movie_repo.find_by_id.assert_called_once_with("1")
    # Le repo de genre NE DOIT PAS être appelé
    mock_genre_repo.list.assert_not_called()

    # Seul le helper de résumé a été appelé
    mock_summary.assert_called_once()
    mock_opinion.assert_not_called()
    mock_genre.assert_not_called()
    mock_tags.assert_not_called()

    # Le résultat est correct
    assert result['id'] == strawberry.ID("1")
    assert result['aiSummary'] == "Résumé IA"
    assert result['aiOpinionSummary'] is None


@pytest.mark.asyncio
async def test_service_v2_analyze_movie_full_request(mocker, mock_llm, mock_movie, mock_genres):
    """
    Teste analyze_movie V2 avec une demande complète.
    Vérifie que tout est appelé (y compris asyncio.gather).
    """
    # 1. Mocker les dépendances (repositories)
    mock_movie_repo = AsyncMock()
    mock_movie_repo.find_by_id.return_value = mock_movie
    mocker.patch('app.services.movie_analyzer_v2.movie_repository', mock_movie_repo)

    mock_genre_repo = AsyncMock()
    mock_genre_repo.list.return_value = mock_genres
    mocker.patch('app.services.movie_analyzer_v2.genre_repository', mock_genre_repo)

    # 2. Mocker les helpers LLM
    mocker.patch('app.services.movie_analyzer_v2.get_ai_summary', AsyncMock(return_value="Résumé IA"))
    mocker.patch('app.services.movie_analyzer_v2.get_ai_opinion_summary', AsyncMock(return_value="Opinion IA"))
    mocker.patch('app.services.movie_analyzer_v2.get_ai_best_genre', AsyncMock(return_value="Genre IA"))
    mocker.patch('app.services.movie_analyzer_v2.get_ai_tags', AsyncMock(return_value=["tag1", "tag2"]))

    # 3. Appel du service
    from app.services.movie_analyzer_v2 import analyze_movie
    result = await analyze_movie(
        movie_id="1",
        ai_summary=True,
        ai_opinion_summary=True,
        ai_best_genre=True,
        ai_tags=True,
        llm=mock_llm
    )

    # 4. Assertions
    # Les deux repos ont été appelés
    mock_movie_repo.find_by_id.assert_called_once_with("1")
    mock_genre_repo.list.assert_called_once()  # Appelé car ai_best_genre=True

    # Le résultat est complet
    assert result['aiSummary'] == "Résumé IA"
    assert result['aiOpinionSummary'] == "Opinion IA"
    assert result['aiBestGenre'] == "Genre IA"
    assert result['aiTags'] == ["tag1", "tag2"]