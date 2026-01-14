from fastapi import FastAPI
from app.core.config import settings
from strawberry.fastapi import GraphQLRouter
import strawberry
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.graphql.context import get_context
from app.graphql.extensions import BusinessLogicErrorExtension
from app.graphql.mutations import Mutation
from app.graphql.queries import Query

# Crée l'application FastAPI
app = FastAPI(
    title="Movie AI GraphQL API",
    description="API GraphQL pour l'analyse de films par IA",
    version="1.0.0",
    debug=settings.DEBUG,
)

# CORS middleware - configured for production
origins = [
    "https://app.tp.k0li.fr",
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crée le schéma GraphQL avec les types de requêtes et de mutations
schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[BusinessLogicErrorExtension]
)

# Crée le routeur GraphQL et l'ajoute à l'application
graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenue sur l'API de l'Analyseur IA de films. Rendez-vous sur /graphql"}


@app.get("/health", tags=["Health"])
def health_check():
    """Endpoint de health check pour Kubernetes liveness/readiness probes."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
    )
