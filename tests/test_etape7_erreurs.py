"""
Tests de validation pour l'Étape 7 (Bonus) : Gestion fine des erreurs métier

Objectif :
1. Vérifier que le service V2 lève bien une `NotFoundBLLException`
   si le `movie_repository` retourne `None`.

Prérequis :
- La logique de gestion d'erreur est en place dans
  `app/services/movie_analyzer_v2.py`.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.core.exceptions import NotFoundBLLException


@pytest.mark.asyncio
async def test_service_v2_raises_not_found(mocker):
    """
    Vérifie que le service `analyze_movie` lève une `NotFoundBLLException`
    si le film n'est pas trouvé dans le repository.
    """
    # 1. Mocker les dépendances (repositories)
    mock_movie_repo = AsyncMock()
    mock_movie_repo.find_by_id.return_value = None  # Simule un film non trouvé
    mocker.patch('app.services.movie_analyzer_v2.movie_repository', mock_movie_repo)

    mock_llm = MagicMock()

    # 2. Appel du service en s'attendant à une exception
    from app.services.movie_analyzer_v2 import analyze_movie

    with pytest.raises(NotFoundBLLException) as exc_info:
        await analyze_movie(
            movie_id="999",
            ai_summary=True,  # Peu importe les drapeaux
            ai_opinion_summary=False,
            ai_best_genre=False,
            ai_tags=False,
            llm=mock_llm
        )

    # 3. Assertions
    # Vérifie que le repo a bien été appelé
    mock_movie_repo.find_by_id.assert_called_once_with("999")
    # Vérifie que le type d'exception est correct
    assert exc_info.type is NotFoundBLLException
    # Vérifie que le message d'erreur contient l'ID
    assert "999" in str(exc_info.value)
    assert "Movie" in str(exc_info.value)