import os
import json
import urllib.request
import urllib.parse
import boto3

s3 = boto3.client("s3")
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/876332050529/swapistackqueue'
bucket_name = 'swapistackbucket'

def lambda_handler(event,context):
    
    for record in event['Records']:
        data = json.loads(record['body'])
        print('Received data:', data)
    
    film_url = urllib.parse.urljoin(data["base_url"],data["extension"])
    
    # Fetch Data from SWAPI
    response = urllib.request.urlopen(film_url)
    response_data = response.read()
    response_json = json.loads(response_data)

    # Read Film Data
    films = response_json["results"][:1]

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
        
        film_actor = {"title": film_title,"actors": actor_names}
        
        print(json.dumps(film_actor, indent=4)) 
        
        #DATA as Message to SQS
        message_body = json.dumps(film_actor)
        
        #Upload files to S3 Bucket
        s3.put_object(Bucket = bucket_name, Key = folder+film_filename, Body = message_body )
        
    return {
        "statusCode": 200,
        "body": "JSON Files Uploaded Succesfully to S3 Bucket with SQS Message"
    }
