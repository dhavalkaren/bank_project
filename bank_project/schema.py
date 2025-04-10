import graphene
import banks.schema


class Query(
    banks.schema.Query,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query)