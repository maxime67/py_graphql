from typing import List
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Classe de configuration qui charge les variables d'environnement.
    """

    # Configuration du modèle Pydantic
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    # Paramètres du projet
    PROJECT_NAME: str = "FastAPI GraphQL LLM Project"

    # Configuration de LM Studio (serveur Chat local)
    LLM_CHAT_SERVER_BASE_URL: str = "http://127.0.0.1:1234/v1"
    LLM_CHAT_MODEL: str = "gemma-3-1b-it-qat" # ou "meta-llama-3.1-8b-instruct"
    LLM_CHAT_TEMPERATURE: float = 0.3 # On baisse un peu la température pour des résultats plus prévisibles (mais moins créatifs)
    LLM_CHAT_API_KEY: str = "not-needed" # Clé API factice, LM Studio ne l'utilise pas

    # Configuration de l'API
    MOVIE_API_BASE_URL: str = "http://127.0.0.1:8000/api/v1"

    # Configuration CORS
    # Pydantic va automatiquement convertir la chaîne de caractères séparée par des virgules
    # en une liste de chaînes de caractères.
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

settings = Settings()
