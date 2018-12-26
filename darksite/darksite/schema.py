import graphene

import account.schema
import cms.schema
import cms.blog.schema
import teams.schema


class Mutation(account.schema.Mutations, teams.schema.Mutations):
    pass


class Query(
    account.schema.Query,
    cms.schema.Query,
    cms.blog.schema.Query,
    graphene.ObjectType,
):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
