import strawberry
from typing import Optional

# Cette classe utilisée par les resolvers, représente l'input pour une opération liée à un film
# Elle contient uniquement l'ID du film
# Elle est donnée à titre indicatif et peut être étendue avec d'autres champs si nécessaire.

@strawberry.input
class MovieInput:
    id: strawberry.ID

