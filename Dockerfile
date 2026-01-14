# syntax=docker/dockerfile:1
FROM python:3.13-slim

# Métadonnées
LABEL maintainer="maxxa"
LABEL description="FastAPI GraphQL LLM API pour l'analyse de films"

# Variables d'environnement pour Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

# Variables d'environnement par défaut (peuvent être surchargées)
ENV HOST=0.0.0.0 \
    PORT=8001 \
    LOG_LEVEL=info \
    WORKERS=1 \
    DEBUG=false

# Répertoire de travail
WORKDIR /app

# Installer uv pour la gestion des dépendances
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copier les fichiers de configuration des dépendances
COPY pyproject.toml uv.lock* ./

# Installer les dépendances (production uniquement)
RUN uv sync --frozen --no-cache --no-dev

# Copier le code de l'application
COPY ./src/app ./app

# Créer un utilisateur non-root pour la sécurité
RUN adduser --disabled-password --gecos "" --uid 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Exposer le port (utilise la variable d'environnement PORT)
EXPOSE ${PORT}

# Health check pour Kubernetes
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/health')" || exit 1

# Commande de démarrage avec gunicorn pour la production
CMD ["sh", "-c", "uv run gunicorn app.main:app --workers ${WORKERS} --worker-class uvicorn.workers.UvicornWorker --bind ${HOST}:${PORT} --access-logfile - --error-logfile - --log-level ${LOG_LEVEL}"]
