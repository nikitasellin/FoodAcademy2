import graphene

from users.schema import Query as UsersQuery
from courses.schema import Query as CoursesQuery


class Query(UsersQuery, CoursesQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
