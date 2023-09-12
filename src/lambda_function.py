import os
import json
import urllib.request
import boto3

#boto3 clients
s3 = boto3.client("s3")
sqs = boto3.client("sqs")

#S3 Bucket Name
bucket_name = 'swapistackbucket'

#SQS Queue Name
queue_name = 'swapistackqueue'    
queue_url = f"https://sqs.us-east-1.amazonaws.com/876332050529/{queue_name}"

#SWAPI Film Data URL
film_url = "https://swapi.dev/api/films/"

def lambda_handler(event,context):

    for record in event['Records']:
        data = json.loads(record['body'])
        print('Received data:', data)
    
    #from lambda_sqs_trigger
    for message in event['Records']:
        data = json.loads(message['body'])
        print('Received data:', data)

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
        sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message_body))
        
        #Upload files to S3 Bucket
        s3.put_object(Bucket = bucket_name, Key = folder+film_filename, Body = message_body )
        
    return {
        "statusCode": 200,
        "body": "JSON Files Uploaded Succesfully to S3 Bucket with SQS Message"
    }
  