import os
import json
import urllib.request
import boto3

def lambda_handler(event,context):
    s3 = boto3.client("s3")
    bucket_name = "travel1s3bucket" 
    
    film_url = "https://swapi.dev/api/films/"
    
    # Data from SWAPI
    response = urllib.request.urlopen(film_url)
    response_data = response.read()
    response_json = json.loads(response_data)

    # Read Film Data
    films = response_json["results"][:3]

    # Iterating Films and Storing
    for film in films:
        film_title = film["title"]
        character_urls = film["characters"]
        film_filename = f"{film_title.replace(' ', '_')}.json"
        folder = "Film_Data/"
        actor_names = []

        # Character Iteration
        for character_url in character_urls:
            character_response = urllib.request.urlopen(character_url)
            character_data = json.loads(character_response.read())
            actor_names.append(character_data["name"])
                
        print(actor_names)
        
        film_actor = {"title": film_title,"actors": actor_names}
        
        #Save to JSON
        uploadByteStream = bytes(json.dumps(film_actor).encode('UTF-8'))
            
        s3.put_object(Bucket = bucket_name, Key = folder+film_filename, Body = uploadByteStream )
            
    return {
        "statusCode": 200,
        "body": "JSON Files Uploaded to S3"
    }