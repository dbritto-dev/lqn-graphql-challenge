# Built-in package

# Third-party packages
import graphene as gql
from django.db.transaction import atomic

# Local packages
from api_v1.domain.person import models, types
from api_v1.domain.person.data import (
    create_person,
    get_person,
    update_person,
    delete_person,
)


class CreatePerson(types.PersonOutputMutation, gql.Mutation):
    class Arguments:
        data = types.PersonCreateInput(required=True)

    @atomic
    # skipcq: PYL-E0213, PYL-R0201
    def mutate(
        _root: models.Person, _info: gql.ResolveInfo, data: types.PersonCreateInput
    ) -> models.Person:
        return create_person(data)


class UpdatePerson(types.PersonOutputMutation, gql.Mutation):
    class Arguments:
        data = types.PersonUpdateInput(required=True)
        where = types.PersonWhereUniqueInput(required=True)

    @atomic
    # skipcq: PYL-E0213, PYL-R0201
    def mutate(
        _root: models.Person,
        _info: gql.ResolveInfo,
        where: types.PersonWhereUniqueInput,
        data: types.PersonUpdateInput,
    ) -> models.Person:
        return update_person(where, data)


class DeletePerson(types.PersonOutputMutation, gql.Mutation):
    class Arguments:
        where = types.PersonWhereUniqueInput(required=True)

    @atomic
    # skipcq: PYL-E0213, PYL-R0201
    def mutate(
        _root: models.Person,
        _info: gql.ResolveInfo,
        where: types.PersonWhereUniqueInput,
    ) -> models.Person:
        return delete_person(where)


class Query(gql.ObjectType):
    person = gql.Field(types.Person, where=types.PersonWhereUniqueInput(required=True))
    persons = types.PersonFilterConnectionField(
        types.Person, where=types.PersonWhereInput()
    )

    def resolve_person(
        _root: models.Person,
        _info: gql.ResolveInfo,
        where: types.PersonWhereUniqueInput,
    ):
        return get_person(where)


class Mutation(gql.ObjectType):
    create_person = CreatePerson.Field(required=True)
    update_person = UpdatePerson.Field()
    delete_person = DeletePerson.Field()
