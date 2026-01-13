
async def analyze_movie(movie_id: str) -> dict:
    return {
        "id": movie_id,
        "aiSummary": "Ceci est un résumé statique du film.",
        "aiOpinionSummary": "Ceci est un résumé statique des avis.",
        "aiBestGenre": "Action",
        "aiTags": ["tag1", "tag2", "tag3"]
    }
