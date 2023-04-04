import graphene
from bson import ObjectId
from mongoengine import connect, disconnect
from schemas import Country
from graphene_types import CountryOutputType
from utils import DB_CONNECTION_STRING

# It defines the Mutation object that contains the fields to be updated
class EditCountry(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.JSONString()
        independent = graphene.Boolean()
        status = graphene.Boolean()
        unMember = graphene.Boolean()
        currencies = graphene.JSONString()
        capital = graphene.List(graphene.String)
        languages = graphene.List(graphene.String)
        latlng = graphene.List(graphene.Float)
        flag = graphene.String()
        maps = graphene.JSONString()
        population = graphene.Int()
        timezones = graphene.List(graphene.String)
        continents = graphene.List(graphene.String)

    country = graphene.Field(CountryOutputType)

    def mutate(self, info, **kwargs):
        connect(host=DB_CONNECTION_STRING)
        document_id = ObjectId(kwargs.get('id'))
        country = Country.objects.get(id=document_id)
        for key, value in kwargs.items():
            if key != "id":
                setattr(country, key, value)
        country.save()
        disconnect()
        return EditCountry(country=country)


# It defines the Mutation object that contains the fields that can be updated.
class Mutation(graphene.ObjectType):
    countryEditMutation = EditCountry.Field()