from mongoengine import (
    BooleanField, DictField, Document, 
    FloatField, IntField, ListField, StringField, queryset_manager
)

# It's a class that represents a country
class Country(Document):
    name = DictField()
    independent = BooleanField(default=True)
    status = BooleanField(default=True)
    unMember = BooleanField(default=False)
    currencies = DictField()
    capital = ListField(StringField(), default=list)
    languages = ListField(StringField(), default=list)
    latlng = ListField(FloatField(), default=list)
    flag = StringField(max_length=10)
    maps = DictField()
    population = IntField()
    timezones = ListField(StringField(max_length=15), default=list)
    continents = ListField(StringField(max_length=15), default=list)

    @queryset_manager
    def with_distance(cls, queryset, lat, lng):
        """
        It takes a queryset, and returns a queryset with a new field called distance
        
        :param cls: The class of the model that the queryset is for
        :param queryset: The queryset that is being filtered
        :param lat: latitude of the user
        :param lng: longitude
        :return: A queryset of documents with a new field called distance.
        """
        from utils import get_distance
        for doc in queryset:
            doc.distance = get_distance(doc, lat, lng)
        return queryset
