import requests, math, os
from mongoengine import connect, disconnect
from mongoengine.errors import ValidationError
from schemas import Country
from dotenv import load_dotenv

load_dotenv()

DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING', 'mongodb://127.0.0.1:27017/countries_db')

def fetch_countries():
    """
    It fetches the data from the API endpoint and returns the data in JSON format
    :return: A list of dictionaries
    """
    # Fetch the data from the API endpoint
    data = None
    try:
        url = 'https://restcountries.com/v3.1/all'
        response = requests.get(url)
        data = response.json()
    except Exception as e:
        print(e)
    return data

def clean_data(item):
    """
    If all the keys in the key_list are present in the item, then create a new dictionary with the keys in key_list and the values from item
    
    :param item: The dictionary that contains the data for a single country

    :return: A tuple of two values. The first value is a dictionary of the cleaned data. The second value is a boolean
    value that indicates whether the data is clean or not.
    """
    cleaned_data, is_clean = None, False
    key_list = ['name', 'independent', 'status', 'status', 'unMember', 
                'currencies', 'capital', 'languages', 'latlng', 'flag', 
                'maps', 'population', 'timezones', 'continents']

    if all(key in item for key in key_list):
        cleaned_data = {k: [vl for ky, vl in item[k].items()] if k == "languages" else item[k] for k in key_list}
        is_clean = True
    return cleaned_data, is_clean

def add_collections(data):
    """
    It takes a list of dictionaries as an argument, connects to MongoDB, cleans the data, validates it, and saves it to the
    database
    
    :param data: The data to be added to the database
    """
    if data:
        print("Creating MongoDB connection")
        connect(host=DB_CONNECTION_STRING)
        for item in data:
            cleaned_data, is_clean = clean_data(item)
            if is_clean:
                country = Country(**cleaned_data)
                try:
                    country.clean()
                    country.save()
                except ValidationError as e:
                    print(e)
        print("Colletion added to DB")
        disconnect()
        print("Disconnecting MongoDB connection")

        
#Function to insert data collected from Countries REST API into MongoDB
def insert_data_into_db():
    """
    It fetches data from an API and inserts it into a database
    """
    print("Please wait fetching country list")
    countries_data = fetch_countries()
    print("Country list fetched successfully.")
    add_collections(countries_data)

def get_distance(country, input_lat, input_lng):
    """
    It calculates the distance between two points on the Earth's surface, given their latitude and longitude
    
    :param country: the country object from the list of countries
    :param input_lat: The latitude of the input location
    :param input_lng: The longitude of the point you want to find the closest country to
    :return: The distance between the inputted coordinates and the country's coordinates.
    """
    country_lat = country["latlng"][0]
    country_lng = country["latlng"][1]
    d_lat = math.radians(country_lat - input_lat)
    d_lng = math.radians(country_lng - input_lng)
    a = math.sin(d_lat / 2) ** 2 + math.cos(math.radians(input_lat)) * math.cos(math.radians(country_lat)) * math.sin(d_lng / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = 6371 * c
    return distance

def get_nearest_countries(input_lat, input_lng):
    """
    It connects to the MongoDB database, and then uses the Country model to find the nearest countries to the input
    latitude and longitude
    
    :param input_lat: latitude of the point of interest
    :param input_lng: longitude of the point of interest
    :return: A list of countries with their distance from the input coordinates.
    """
    connect(host=DB_CONNECTION_STRING)
    countries =  list(Country.with_distance(input_lat, input_lng))
    return countries

def get_countries_by_language(language):
    """
    It connects to the database, finds all the countries that have a language that matches the language parameter, and
    returns the countries
    
    :param language: The language you want to search for
    :return: A list of countries that have the language in their languages list.
    """
    connect(host=DB_CONNECTION_STRING)
    countries = Country.objects(languages__in=[language])
    return countries