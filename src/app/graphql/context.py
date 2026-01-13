from fastapi import Request
from typing import Any, Dict
from app.core.llm import llm

async def get_context(request: Request) -> Dict[str, Any]:
    """
    Crée le contexte pour chaque requête GraphQL.
    """
    return {
        "request": request,
        "llm": llm  # on ajoute l'instance llm au dictionnaire du contexte
    }
