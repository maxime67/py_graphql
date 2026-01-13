import strawberry
from strawberry import Info

# from app.graphql.inputs.movie_input import MovieInput
from app.graphql.types.movie_analysis import MovieAnalysis
from app.services.movie_analyzer_v1 import analyze_movie

async def analyze_movie_by_id(
    movie_id: strawberry.ID,
    # movie_input: MovieInput, classe nécessaire seulement si on avait eu beaucoup de champs en entrée
) -> MovieAnalysis:

    analysis_data = await analyze_movie(movie_id=movie_id)
    return MovieAnalysis(**analysis_data)