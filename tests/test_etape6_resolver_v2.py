"""
Tests de validation pour l'Étape 6 : Optimisation du Resolver GraphQL (Version 2)

Objectif :
1. Vérifier que le resolver V2 récupère bien le LLM du contexte.
2. Vérifier que le resolver V2 utilise `is_field_requested` pour
   passer les bons booléens au service V2.

Prérequis :
- Les TODOs de `app/graphql/resolvers/analyze_movie_v2.py` sont complétés.
- Le champ `analyzeMovie` de `app/graphql/queries.py` est mis à jour
  pour utiliser le resolver V2.
"""

import pytest
import strawberry
from unittest.mock import AsyncMock, MagicMock, patch

@pytest.fixture
def mock_info():
    """Fixture pour un objet Info de Strawberry."""
    mock_llm_instance = MagicMock(name="MockLLM")
    info = MagicMock()
    info.context = {"llm": mock_llm_instance}
    return info

@pytest.mark.asyncio
async def test_resolver_v2_partial_request(mocker, mock_info):
    """
    Teste le resolver V2 avec une requête partielle.
    Vérifie qu'il passe les bons drapeaux au service.
    """
    # 1. Mocker les dépendances (le service V2 et le helper is_field_requested)

    # On mock le service V2 pour espionner ses arguments
    mock_service = AsyncMock(return_value={
        "id": "1",
        "aiSummary": "Service Result",
        "aiOpinionSummary": None,
        "aiBestGenre": None,
        "aiTags": None
    })
    mocker.patch('app.graphql.resolvers.analyze_movie_v2.analyze_movie', mock_service)

    # On mock 'is_field_requested' pour simuler une requête partielle
    def mock_is_field_requested(info, field_name):
        if field_name == "aiSummary":
            return True
        return False

    mocker.patch('app.graphql.resolvers.analyze_movie_v2.is_field_requested', mock_is_field_requested)

    # 2. Appel du resolver
    from app.graphql.resolvers.analyze_movie_v2 import analyze_movie_by_id

    await analyze_movie_by_id(
        movie_id=strawberry.ID("1"),
        info=mock_info
    )

    # 3. Assertions
    # Vérifie que le service a été appelé avec les bons drapeaux
    mock_service.assert_called_once_with(
        movie_id="1",
        ai_summary=True,
        ai_opinion_summary=False,
        ai_best_genre=False,
        ai_tags=False,
        llm=mock_info.context["llm"] # Vérifie que le LLM du contexte est bien passé
    )

@pytest.mark.asyncio
async def test_resolver_v2_full_request(mocker, mock_info):
    """
    Teste le resolver V2 avec une requête complète.
    """
    # 1. Mocker les dépendances
    # [CORRECTION] Le mock doit retourner un dictionnaire complet
    # pour que MovieAnalysis(**analysis_data) fonctionne.
    mock_service_return = {
        "id": "1",
        "aiSummary": "Mock summary",
        "aiOpinionSummary": "Mock opinion",
        "aiBestGenre": "Mock genre",
        "aiTags": ["mock", "tag"]
    }
    mock_service = AsyncMock(return_value=mock_service_return)
    mocker.patch('app.graphql.resolvers.analyze_movie_v2.analyze_movie', mock_service)

    # Simule une requête complète
    mocker.patch('app.graphql.resolvers.analyze_movie_v2.is_field_requested', return_value=True)

    # 2. Appel du resolver
    from app.graphql.resolvers.analyze_movie_v2 import analyze_movie_by_id

    await analyze_movie_by_id(
        movie_id=strawberry.ID("1"),
        info=mock_info
    )

    # 3. Assertions
    # Vérifie que le service a été appelé avec TOUS les drapeaux à True
    mock_service.assert_called_once_with(
        movie_id="1",
        ai_summary=True,
        ai_opinion_summary=True,
        ai_best_genre=True,
        ai_tags=True,
        llm=mock_info.context["llm"]
    )