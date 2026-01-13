FROM python:3.9

WORKDIR /code

# Installer uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copier les fichiers de configuration des dépendances
COPY pyproject.toml uv.lock* ./

# Installer les dépendances
RUN uv sync --frozen --no-cache

# Copier le code de l'application
COPY ./src/app /code/app

# Exposer le port
EXPOSE 80

# Lancer l'application avec uvicorn
CMD ["uv", "run", "fastapi", "run", "app/main.py", "--port", "80"]