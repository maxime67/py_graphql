from typing import List
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Classe de configuration qui charge les variables d'environnement.
    Toutes les valeurs peuvent être surchargées via des variables d'environnement
    pour une utilisation en conteneur (Docker/Kubernetes).
    """

    # Configuration du modèle Pydantic
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Paramètres du projet
    PROJECT_NAME: str = "FastAPI GraphQL LLM Project"
    DEBUG: bool = False

    # Configuration du serveur
    HOST: str = "0.0.0.0"
    PORT: int = 8002
    LOG_LEVEL: str = "info"
    WORKERS: int = 1

    # Configuration de LM Studio (serveur Chat local)
    LLM_CHAT_SERVER_BASE_URL: str = "http://127.0.0.1:1234/v1"
    LLM_CHAT_MODEL: str = "qwen3-4b-instruct-2507"
    LLM_CHAT_TEMPERATURE: float = 0.3
    LLM_CHAT_API_KEY: str = "not-needed"
    LLM_CHAT_TIMEOUT: int = 60

    # Configuration de l'API externe (Movie API)
    MOVIE_API_BASE_URL: str = "http://127.0.0.1:8000/api/v1"
    MOVIE_API_TIMEOUT: int = 30

    # Configuration CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Configuration Health Check
    HEALTH_CHECK_PATH: str = "/health"


settings = Settings()
