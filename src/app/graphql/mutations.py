import strawberry

from app.graphql.resolvers.noop import resolve_noop


@strawberry.type
class Mutation:
    """
    Point d'entrée pour toutes les mutations GraphQL.
    """
    _noop: bool = strawberry.field(
        resolver=resolve_noop,
        description="Mutation factice pour assurer la validité du schéma."
    )