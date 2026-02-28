import requests
import random
from PIL import Image
from io import BytesIO
import urllib.parse

def get_artist_objectIDs(artist_name):
    quoted_name = urllib.parse.quote(artist_name)
    print
    search_url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?artistOrCulture=true&q={quoted_name}"
    search_response = requests.get(search_url)
    print(f"Search URL: {search_url}")
    search_data = search_response.json()
 
    if not search_data.get('objectIDs'):
        print(f"No objects found for artist: {artist_name}")
        return None
    
    return search_data.get('objectIDs')
    
def get_random_objectID(objectIDs):    
    random_objectID = random.choice(objectIDs)
    return random_objectID

def get_object_details(objectID):
    object_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{objectID}"
    object_response = requests.get(object_url)
    print(f"Object URL: {object_url}")
    object_data = object_response.json()
    return object_data

def get_random_artwork_from_artist(artist_name):
    objectIDs = get_artist_objectIDs(artist_name)
    if not objectIDs:
        print(f"No artworks found for artist: {artist_name}")

        result = {
            "artist_name": artist_name,
            "title": f"No artworks by {artist_name} found in the Met Museum collection. We sincerely apologize for the inconvenience.",
            "image_url": "https://collectionapi.metmuseum.org/api/collection/v1/iiif/461589/915596/main-image"
        }
        return result
    
    random_objectID = get_random_objectID(objectIDs)

    object_data = get_object_details(random_objectID)
    
    image_url = object_data.get('primaryImageSmall')
    print (f"Image URL: {image_url}")
    title = object_data.get('title')
    
    result = {
        "artist_name": artist_name,
        "title": title,
        "image_url": image_url
    }
    return result

get_random_artwork_from_artist_function = {
    "name": "get_random_artwork_from_artist",
    "description": "Get a random artwork from the given artist. Returns the title of the artwork and a URL to an image of the artwork. The url will be used to display the image in the chat interface.",
    "parameters": {
        "type": "object",
        "properties": {
            "artist_name": {
                "type": "string",
                "description": "The name of the artist to get a random artwork from.",
            },
        },
        "required": ["artist_name"],
        "additionalProperties": False
    }
}

def get_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

