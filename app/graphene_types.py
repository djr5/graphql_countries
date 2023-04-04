import graphene


# The above code defines a custom scalar for dictionaries in Python using the graphene library.
class CustomDictionary(graphene.Scalar):
    # Define custom scalar for dictionaries
    pass

# This is a GraphQL object type representing a country with various fields and corresponding resolver functions.

class CountryType(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    independent = graphene.Boolean()
    status = graphene.Boolean()
    unMember = graphene.Boolean()
    currencies = CustomDictionary()
    capital = graphene.List(graphene.String)
    languages = graphene.List(graphene.String)
    latlng = graphene.List(graphene.Float)
    flag = graphene.String()
    maps = CustomDictionary()
    population = graphene.Int()
    timezones = graphene.List(graphene.String)
    continents = graphene.List(graphene.String)

    def resolve_id(self, info):
        return self.id

    def resolve_name(self, info):
        return self.name

    def resolve_independent(self, info):
        return self.independent

    def resolve_status(self, info):
        return self.status

    def resolve_unMember(self, info):
        return self.unMember

    def resolve_currencies(self, info):
        return self.currencies

    def resolve_capital(self, info):
        return self.capital

    def resolve_languages(self, info):
        return self.languages

    def resolve_latlng(self, info):
        return self.latlng

    def resolve_flag(self, info):
        return self.flag

    def resolve_population(self, info):
        return self.population

    def resolve_timezones(self, info):
        return self.timezones

    def resolve_continents(self, info):
        return self.continents


# The NearestCountryType class extends the CountryType class and adds a distance attribute that can be resolved to return
# the distance value.
class NearestCountryType(CountryType):
    distance = graphene.Float()

    def resolve_distance(self, info):
        return self.distance


# This is a GraphQL object type representing various properties of a country.
class CountryOutputType(graphene.ObjectType):
    id = graphene.ID()
    name = CustomDictionary()
    independent = graphene.Boolean()
    status = graphene.Boolean()
    unMember = graphene.Boolean()
    currencies = CustomDictionary()
    capital = graphene.List(graphene.String)
    languages = graphene.List(graphene.String)
    latlng = graphene.List(graphene.Float)
    flag = graphene.String()
    maps = CustomDictionary()
    population = graphene.Int()
    timezones = graphene.List(graphene.String)
    continents = graphene.List(graphene.String)
