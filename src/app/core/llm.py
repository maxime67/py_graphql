from app.core.config import settings
from langchain_openai import ChatOpenAI

# --- Initialisation du Modèle de Langage (LLM) ---
# Cette instance unique sera créée au démarrage de l'application et partagée par toutes les requêtes.
llm = ChatOpenAI(
    model=settings.LLM_CHAT_MODEL,
    base_url=settings.LLM_CHAT_SERVER_BASE_URL,
    temperature=settings.LLM_CHAT_TEMPERATURE,
    api_key=settings.LLM_CHAT_API_KEY
)
