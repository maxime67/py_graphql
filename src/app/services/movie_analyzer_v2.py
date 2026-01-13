import asyncio
import strawberry
from langchain_core.language_models import BaseChatModel
from app.core.exceptions import NotFoundBLLException
from app.repositories.movie_repository import movie_repository
from app.repositories.genre_repository import genre_repository

async def get_ai_summary(llm, synopsis):
    if not synopsis:
        return None
    prompt = f"""
        Français uniquement.
        Fais un résumé très court (une à deux phrases maximum) du synopsis suivant.
        Ne retourne que le résumé, sans aucune phrase d'introduction comme "Voici le résumé :".

        Synopsis : {synopsis}
        """
    response = await llm.ainvoke(prompt)
    return response.content.strip()

async def get_ai_opinion_summary(llm, title, opinions):
    if not opinions:
        return None
    opinions_text = "\n".join([f"ID Opinion = {opinion.id}; Note : {opinion.note}/5; Commentaire : {opinion.comment}" for opinion in opinions])
    prompt = f"""
        Français uniquement.
        Fais un résumé très court (une à deux phrases maximum) des opinions suivantes. Les opinions portent sur un même et unique film, dont le titre est : {title}. 
        Ne fais pas une liste d'items. Ne fais pas un résumé de chaque opinion individuellement, mais un résumé global.
        Ne retourne que le résumé, sans aucune phrase d'introduction comme "Voici le résumé :".
        Opinions :
        {opinions_text}
    """
    response = await llm.ainvoke(prompt)
    return response.content.strip()

async def get_ai_best_genre(llm, synopsis, all_genres):
    if not synopsis or not all_genres:
        return None

    # Préparation de la liste des genres pour le prompt
    genres_list = ", ".join([genre.label for genre in all_genres])

    # Prompt pour choisir le genre le plus pertinent
    prompt = f"""
        Français uniquement.
        Choisis le genre le plus pertinent pour le film parmi la liste fournie.
        Tu dois choisir EXCLUSIVEMENT un genre de la liste fournie.
        Ne retourne QUE le nom du genre, sans aucune phrase d'introduction.

        Voici le synopsis :
        {synopsis}

        Voici la liste des genres autorisés :
        {genres_list}

        Genre le plus pertinent :
        """

    # Appel asynchrone au modèle de langage
    response = await llm.ainvoke(prompt)
    return response.content.strip()


async def get_ai_tags(llm, title, synopsis):
    if not title or not synopsis:
        return None

    prompt = f"""
        Français uniquement.
        Génère 5 tags pertinents pour le film.
        Retourne une liste de tags séparés par des virgules.
        Ne retourne que les tags, sans aucune phrase d'introduction.

        Titre du film : {title}
        Synopsis : {synopsis}

        Génère 5 tags pertinents, séparés par des virgules :
        """

    response = await llm.ainvoke(prompt)
    tags = [tag.strip() for tag in response.content.split(',') if tag.strip()]
    return tags


async def analyze_movie(
        movie_id : str,
        ai_summary: bool,
        ai_opinion_summary : bool,
        ai_best_genre : bool,
        ai_tags : bool,
        llm: BaseChatModel
) -> dict:

    # Récupération des genres
    all_genres = []
    if ai_best_genre:
        all_genres = await genre_repository.list()

    # Récupération des données du film
    movie_data = await movie_repository.find_by_id(movie_id)
    if not movie_data:
        raise NotFoundBLLException(resource_name="Movie", resource_id=movie_id)

    # Tâches à effectuer
    tasks = {}

    if ai_summary:
        tasks["aiSummary"] = get_ai_summary(llm, movie_data.synopsis)

    if ai_opinion_summary:
        tasks["aiOpinionSummary"] = get_ai_opinion_summary(llm, movie_data.title, movie_data.opinions)

    if ai_best_genre:
        tasks["aiBestGenre"] = get_ai_best_genre(llm, movie_data.synopsis, all_genres)

    if ai_tags:
        tasks["aiTags"] = get_ai_tags(llm, movie_data.title, movie_data.synopsis)

    if tasks:
        # On récupère les coroutines (les fonctions async prêtes à être lancées)
        coroutines = tasks.values()
        # On les exécute toutes en parallèle et on attend les résultats
        results = await asyncio.gather(*coroutines)
        # On associe les résultats aux clés que nous avons définies
        result_map = dict(zip(tasks.keys(), results))
    else:
        result_map = {}  # Aucune tâche n'a été demandée

    output = {
        'id': strawberry.ID(movie_id),
        'aiSummary': result_map.get("aiSummary"),
        'aiOpinionSummary': result_map.get("aiOpinionSummary"),
        'aiBestGenre': result_map.get("aiBestGenre"),
        'aiTags': result_map.get("aiTags")
    }

    print(output)

    return output
