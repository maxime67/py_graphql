import strawberry

# Note : l'énoncé demande d'importer la V1 à l'étape 3, puis la V2 à l'étape 6
# L'import ci-dessous correspond à l'étape 6.
from app.graphql.resolvers.analyze_movie_v2 import analyze_movie_by_id
from app.graphql.types.movie_analysis import MovieAnalysis


@strawberry.type
class Query:
    """
    Point d'entrée pour toutes les requêtes GraphQL de type 'query'.
    """

    analyzeMovie: MovieAnalysis = strawberry.field(
        resolver=analyze_movie_by_id,
        description="Analyse un film en utilisant l'IA."
    )
