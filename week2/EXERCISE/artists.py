import json
import random

# Load the artists data from JSON file
with open('artists.json', 'r', encoding='utf-8') as file:
    artists = json.load(file)

def get_random_artist():
    return random.choice(artists)

get_random_artist_function = {
    "name": "get_random_artist",
    "description": "Get a random artist from the list of available artists.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    }
}

def get_artist_suggestions(query):
    if len(query) < 3:
        return []
    
    query_lower = query.lower()
    return [artist for artist in artists if query_lower in artist.lower()]

def get_artist(name):
    for artist in artists:
        if artist == name:
            return artist
    return None


ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

def get_ticket_price(destination_city):
    print(f"Tool called for city {destination_city}")
    price = ticket_prices.get(destination_city.lower(), "Unknown ticket price")
    return f"The price of a ticket to {destination_city} is {price}"

# There's a particular dictionary structure that's required to describe our function:
price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}