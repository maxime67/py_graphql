"""
Tests de validation pour l'Étape 3 : Mise en place GraphQL (Version 1 - Statique)

Objectif :
1. Vérifier que le service `movie_analyzer_v1` retourne bien un dict "mock".
2. Vérifier que le resolver `analyze_movie_v1` appelle ce service et
   construit correctement l'objet `MovieAnalysis`.

Prérequis :
- Les TODOs de `app/services/movie_analyzer_v1.py` sont complétés.
- Les TODOs de `app/graphql/resolvers/analyze_movie_v1.py` sont complétés.
- Le champ `analyzeMovie` est bien ajouté à `app/graphql/queries.py`
  (en utilisant le resolver V1).
"""

import pytest
import strawberry
from unittest.mock import AsyncMock
from app.graphql.types.movie_analysis import MovieAnalysis

@pytest.mark.asyncio
async def test_service_v1_analyze_movie():
    """
    Teste le service V1. Il doit retourner un dictionnaire
    contenant les clés requises et l'ID correct.
    """
    from app.services.movie_analyzer_v1 import analyze_movie

    movie_id = "123"
    analysis_data = await analyze_movie(movie_id)

    assert isinstance(analysis_data, dict)
    assert analysis_data["id"] == movie_id
    assert "aiSummary" in analysis_data
    assert "aiOpinionSummary" in analysis_data
    assert "aiBestGenre" in analysis_data
    assert "aiTags" in analysis_data
    assert isinstance(analysis_data["aiTags"], list)

@pytest.mark.asyncio
async def test_resolver_v1_analyze_movie_by_id(mocker):
    """
    Teste le resolver V1. Il doit appeler le service V1 et
    retourner un objet `MovieAnalysis` typé.
    """
    # 1. Mock du service V1 que le resolver est censé appeler
    mock_service_data = {
        "id": "1",
        "aiSummary": "Mock summary",
        "aiOpinionSummary": "Mock opinion",
        "aiBestGenre": "Mock genre",
        "aiTags": ["mock", "test"]
    }
    mock_analyze_service = AsyncMock(return_value=mock_service_data)
    mocker.patch('app.graphql.resolvers.analyze_movie_v1.analyze_movie', mock_analyze_service)

    # 2. Appel du resolver
    from app.graphql.resolvers.analyze_movie_v1 import analyze_movie_by_id

    result = await analyze_movie_by_id(movie_id=strawberry.ID("1"))

    # 3. Assertions
    # Vérifie que le service a bien été appelé
    mock_analyze_service.assert_called_once_with(movie_id="1")

    # Vérifie que le résultat est du bon type
    assert isinstance(result, MovieAnalysis)
    assert result.id == strawberry.ID("1")
    assert result.aiSummary == "Mock summary"
    assert result.aiTags == ["mock", "test"]