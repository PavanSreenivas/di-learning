import os
import json
import urllib.request
import urllib.parse
import boto3


def lambda_handler(event,context):
    
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/876332050529/stackbridgequeue'
    
    data = json.loads(event['body'])
    
    message = json.dumps(data)
    print("Recieved Data\n")
    print(message)
    
    response_code = response["ResponseMetadata"]["HTTPStatusCode"]
    
    if response_code == 200:
        message = "Message recieved from SQS"
    else:
        message = "Error in Receiving Message from SQS"
    
    return {
        "body": json.dumps({
            "statusCode": response_code,
            "message": message)
    }
