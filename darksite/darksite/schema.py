import graphene

import account.schema
import blog.schema


class Query(account.schema.Query, blog.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
