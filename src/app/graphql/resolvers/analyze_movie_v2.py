import strawberry
from strawberry import Info

from app.graphql.resolvers.helper import is_field_requested
from app.graphql.types.movie_analysis import MovieAnalysis
from app.services.movie_analyzer_v2 import analyze_movie


async def analyze_movie_by_id(
        movie_id: strawberry.ID,
        info: Info,
) -> MovieAnalysis:
    llm = info.context["llm"]

    analysis_data = await analyze_movie(
        movie_id=movie_id,
        ai_summary=is_field_requested(info, "aiSummary"),
        ai_opinion_summary=is_field_requested(info, "aiOpinionSummary"),
        ai_best_genre=is_field_requested(info, "aiBestGenre"),
        ai_tags=is_field_requested(info, "aiTags"),
        llm=llm
    )

    return MovieAnalysis(**analysis_data)
