import json
import urllib.request

def lambda_handler(event,handler):
    films_url = "https://swapi.dev/api/films/2"

    #API GET request
    response = urllib.request.urlopen(films_url)

    response_data = response.read()
    response_json = json.loads(response_data)
    film_actor = []

    # Iterating  Movies
    film_name = response_json["title"]
    character_urls = response_json["characters"]
    actor_names = []

    # Iterating characters
    for character_url in character_urls:
        character_response = urllib.request.urlopen(character_url)
        character_data = json.loads(character_response.read())
        actor_names.append(character_data["name"])

    film_actor.append({"films": film_name, "actors": actor_names})

    #Display 
    print(json.dumps(film_actor, indent=4)) 

