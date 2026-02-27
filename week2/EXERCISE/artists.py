import json
import random

# Load the artists data from JSON file
with open('artists.json', 'r', encoding='utf-8') as file:
    artists = json.load(file)

def artist_to_string(artist):
    if not artist:
        print
        return "No artist information available."
    
    name = artist.get('name', 'Unknown Artist')
    years = artist.get('years', 'Unknown Years')
    collection = artist.get('collection', 'Unknown Collection')
    
    result = f"{name}, period in which he/she lived: ({years}), in collection: {collection}."
    print(f"Artist details: {result}")
    return result

def get_random_artist():
    choice = random.choice(artists)
    print(f"Random artist: {choice.get('name', 'Unknown')}")
    return artist_to_string(choice)

get_random_artist_function = {
    "name": "get_random_artist",
    "description": "Get a random artist: his/her name, period in which he/she lived, and the museum collection the artist's work belong to.",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
        "additionalProperties": False
    }
}

def get_artist_suggestions(query):
    if len(query) < 3:
        return artist_to_string(None)
    
    query_lower = query.lower()
    suggestions = [artist for artist in artists if query_lower in artist.get('name', '').lower()]
    print(f"Artist suggestions for '{query}': {[artist.get('name', 'Unknown') for artist in suggestions]}")
    return list(map(artist_to_string, suggestions))

get_artist_suggestions_function = {
    "name": "get_artist_suggestions",
    "description": "Get a list of artists based on a search query. Returns a list of artist's names that contain the query string (minimum 3 characters), period in which he/she lived, and the museum collections the artist's work belong to.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query to find matching artist names (minimum 3 characters)",
            },
        },
        "required": ["query"],
        "additionalProperties": False
    }
}

def get_artist(name):
    for artist in artists:
        if artist.get('name') == name:
            print(f"Found artist: {artist.get('name', 'Unknown')}")
            return artist_to_string(artist)
    print(f"No artist found with name: {name}")
    return artist_to_string(None)


get_artist_function = {
    "name": "get_artist",
    "description": "Get an artist by name from the list of available artists with his/her name, period in which he/she lived, and the museum collection his/her work belong to.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name of the artist to retrieve (exact match)",
            },
        },
        "required": ["name"],
        "additionalProperties": False
    }
}

def parse_years(years_str):
    """Parse a years string like '1375–1444' or 'ca. 1730–1785' and return (start_year, end_year)"""
    import re
    
    # Remove prefixes like "ca.", "circa", etc.
    cleaned = re.sub(r'^(ca\.|circa)\s*', '', years_str, flags=re.IGNORECASE)
    
    # Split on various dash characters (em-dash, en-dash, hyphen)
    years = re.split(r'[–—-]', cleaned)
    
    if len(years) >= 2:
        try:
            start_year = int(years[0].strip())
            end_year = int(years[1].strip())
            return start_year, end_year
        except ValueError:
            return None, None
    elif len(years) == 1:
        try:
            year = int(years[0].strip())
            return year, year
        except ValueError:
            return None, None
    
    return None, None

def years_overlap(years1_str, years2_str, tolerance):
    """Check if two year ranges overlap within a given tolerance"""
    start1, end1 = parse_years(years1_str)
    start2, end2 = parse_years(years2_str)
    
    if None in (start1, end1, start2, end2):
        return False
    
    # Expand ranges by tolerance
    expanded_start1 = start1 - tolerance
    expanded_end1 = end1 + tolerance
    
    # Check if ranges overlap
    return not (end2 < expanded_start1 or start2 > expanded_end1)

def get_contemporary(years):
    """Get a random artist whose period in which he/she lived are roughly contemporary with the given years"""
    tolerances = [50, 100, 250, 500, 1000]
    
    for tolerance in tolerances:
        # Find all artists within the current tolerance
        matching_artists = [
            artist for artist in artists 
            if years_overlap(years, artist.get('years', ''), tolerance)
        ]
        print(f"Found {len(matching_artists)} artists within {tolerance} years tolerance for '{years}'")
        
        if matching_artists:
            chosen_artist = random.choice(matching_artists)
            print(f"Selected contemporary artist: {chosen_artist.get('name', 'Unknown')}")
            return artist_to_string(chosen_artist)
    
    # If nothing found even with 1000 years tolerance
    print(f"No contemporary artist found for '{years}'")
    return artist_to_string(None)

get_contemporary_function = {
    "name": "get_contemporary",
    "description": "Get a random artist object from the list of available artists whose period in which he/she lived are roughly contemporary with the given years. The function will first try to find artists within a 50-year range, then expand to 100 years, 250 years, 500 years, and finally 1000 years if no matches are found.",
    "parameters": {
        "type": "object",
        "properties": {
            "years": {
                "type": "string",
                "description": "The period in which he/she lived to find contemporary artists for (e.g., '1375–1444' or 'ca. 1730–1785')",
            },
        },
        "required": ["years"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": get_artist_function}, {"type": "function", "function": get_contemporary_function}, {"type": "function", "function": get_random_artist_function}, {"type": "function", "function": get_artist_suggestions_function}]

def handle_tool_calls(message):
    responses = []
    for tool_call in message.tool_calls:
        if tool_call.function.name == "get_artist":
            arguments = json.loads(tool_call.function.arguments)
            name = arguments.get('name')
            artist_details = get_artist(name)
            responses.append({
                "role": "tool",
                "content": artist_details,
                "tool_call_id": tool_call.id
            })
        elif tool_call.function.name == "get_contemporary":
            arguments = json.loads(tool_call.function.arguments)
            years = arguments.get('years')
            contemporary_artist = get_contemporary(years)
            responses.append({
                "role": "tool",
                "content": contemporary_artist,
                "tool_call_id": tool_call.id
            })
        elif tool_call.function.name == "get_random_artist":
            random_artist = get_random_artist()
            responses.append({
                "role": "tool",
                "content": random_artist,
                "tool_call_id": tool_call.id
            })
        elif tool_call.function.name == "get_artist_suggestions":
            arguments = json.loads(tool_call.function.arguments)
            query = arguments.get('query')
            suggestions = get_artist_suggestions(query)
            responses.append({
                "role": "tool",
                "content": suggestions,
                "tool_call_id": tool_call.id
            })
    return responses
