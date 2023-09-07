import os
import json
import urllib.request
import boto3

#boto3 clients
s3 = boto3.client("s3")
sqs = boto3.client("sqs")

#s3 bucket name
bucket_name = 'swapibucket1'

#queue name
queue_name = 'swapiqueue'    
queue_url = f"https://sqs.us-east-1.amazonaws.com/876332050529/{queue_name}"

#SWAPI Film Data URL
film_url = "https://swapi.dev/api/films/"

def lambda_handler(event,context):
    
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
        
        film_actor = {"title": film_title,"actors": actor_names}
        
        print(json.dumps(film_actor, indent=4)) 
        
        #Data as Message to SQS
        message_body = json.dumps(film_actor)
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message_body))
        
        #Upload files to S3
        s3.put_object(Bucket = bucket_name, Key = folder+film_filename, Body = message_body )
        
    return {
        "statusCode": 200,
        "body": "JSON Files Uploaded to S3 with SQS Message"
    }