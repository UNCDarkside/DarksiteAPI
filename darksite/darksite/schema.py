import graphene

import account.schema
import cms.schema
import cms.blog.schema


class Query(
    account.schema.Query,
    cms.schema.Query,
    cms.blog.schema.Query,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(query=Query)
