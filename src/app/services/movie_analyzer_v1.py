
async def analyze_movie(movie_id: str) -> dict:
    return {
        "id": movie_id,
        "ai_summary": "Ceci est un résumé statique du film.",
        "ai_opinion_summary": "Ceci est un résumé statique des avis.",
        "ai_best_genre": "Action",
        "ai_tags": ["tag1", "tag2", "tag3"]
    }
