import graphene
from bson import ObjectId
from graphene_types import CountryType, NearestCountryType
from managers import MongoDBConnection
from utils import get_nearest_countries, get_countries_by_language


# It defines the Query object that contains the fields that can be queried.
class Query(graphene.ObjectType):

    countriesQuery = graphene.List(CountryType, page=graphene.Int(), limit=graphene.Int())
    countryQuery = graphene.Field(CountryType, id=graphene.ID(required=True))
    countriesNearbyQuery = graphene.List(
        NearestCountryType, lat=graphene.Float(required=True), lng=graphene.Float(required=True))
    countriesByLanguageQuery = graphene.List(CountryType, language=graphene.String(required=True))

    def resolve_countriesQuery(self, info,  page=None, limit=None):
        """
        It takes the page and limit arguments from the query and uses them to slice the result of the MongoDB query
        
        :param info: This is the request context. It contains the request information, such as the query string, variables,
        operation name, etc
        :param page: The page number to return
        :param limit: The number of results to return
        :return: A list of CountryType objects.
        """
        with MongoDBConnection("countries_db") as db_conn:
            collection = db_conn['country']
            result = collection.find()
            if page and limit:
                start = (page - 1) * limit
                end = start + limit
                result = result[start:end]
            return [CountryType(
                    id=item["_id"],
                    name=item["name"]["common"],
                    independent=item['independent'],
                    status=item['status'],
                    unMember=item['unMember'],
                    currencies=next(iter(item['currencies'].keys())),
                    capital=item['capital'],
                    languages=item['languages'],
                    latlng=item['latlng'],
                    flag=item['flag'],
                    maps=item['maps'],
                    population=item['population'],
                    timezones=item['timezones'],
                    continents=item['continents'],
                ) for item in result]
        
    def resolve_countryQuery(self, info, id):
        """
        It takes the id of a country, finds the country in the database, and returns the country's information
        
        :param info: This is the GraphQLResolveInfo object that contains information about the execution state of the query
        :param id: The id of the country
        :return: A CountryType object
        """
        with MongoDBConnection("countries_db") as db_conn:
            collection = db_conn['country']
            document_id = ObjectId(id)
            item = collection.find_one({'_id': document_id})
            return CountryType(
                    id=item["_id"],
                    name=item["name"]["common"],
                    independent=item['independent'],
                    status=item['status'],
                    unMember=item['unMember'],
                    currencies=next(iter(item['currencies'].keys())),
                    capital=item['capital'],
                    languages=item['languages'],
                    latlng=item['latlng'],
                    flag=item['flag'],
                    maps=item['maps'],
                    population=item['population'],
                    timezones=item['timezones'],
                    continents=item['continents'],
                )
        
    def resolve_countriesNearbyQuery(self, info, lat, lng):
        """
        It takes a latitude and longitude as arguments, uses a helper function to get the nearest countries, sorts them by distance, and returns the top 10 results
        
        :param info: GraphQLResolveInfo
        :param ltd: latitude
        :param lng: longitude
        :return: A list of NearestCountryType objects
        """
        countries = get_nearest_countries(lat, lng)
        sorted_list = sorted([{
                "id":str(item["id"]),
                "name":item["name"]["common"],
                "independent":item['independent'],
                "status":item['status'],
                "unMember":item['unMember'],
                "currencies":next(iter(item['currencies'].keys())),
                "capital":item['capital'],
                "languages":item['languages'],
                "latlng":item['latlng'],
                "flag":item['flag'],
                "maps":item['maps'],
                "population":item['population'],
                "timezones":item['timezones'],
                "continents":item['continents'],
                "distance":float(item.distance)
            } for item in countries], key=lambda x: x["distance"])[1:11]
        return [NearestCountryType(
                    id=item["id"],
                    name=item["name"],
                    independent=item['independent'],
                    status=item['status'],
                    unMember=item['unMember'],
                    currencies=item['currencies'],
                    capital=item['capital'],
                    languages=item['languages'],
                    latlng=item['latlng'],
                    flag=item['flag'],
                    maps=item['maps'],
                    population=item['population'],
                    timezones=item['timezones'],
                    continents=item['continents'],
                    distance=item['distance']
                ) for item in sorted_list]

    def resolve_countriesByLanguageQuery(self, info, language):
        """
        It returns a list of countries that speak the language specified in the query.
        
        :param info: This is the context of the query. It contains the request, the schema, and the root value
        :param lang: String!
        :return: A list of CountryType objects
        """
        countries = get_countries_by_language(language)
        return [CountryType(
                    id=item["id"],
                    name=item["name"]["common"],
                    independent=item['independent'],
                    status=item['status'],
                    unMember=item['unMember'],
                    currencies=item['currencies'],
                    capital=item['capital'],
                    languages=item['languages'],
                    latlng=item['latlng'],
                    flag=item['flag'],
                    maps=item['maps'],
                    population=item['population'],
                    timezones=item['timezones'],
                    continents=item['continents'],
                ) for item in countries]