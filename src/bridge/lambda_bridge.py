import os
import json
import urllib.request
import urllib.parse
import boto3


def lambda_handler(event,context):
    
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/876332050529/BridgeQueue'
    
    message = json.loads(event["Records"][0]["body"])
    print("Recieved Data\n")
    print(message)
    
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1,  
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,  
        WaitTimeSeconds=0  
    )
    
    response_code = response["ResponseMetadata"]["HTTPStatusCode"]
    
    if response_code == 200:
        message = "Message Recieved from SQS"
    else:
        message = "Error in Receiving Message from SQS"
    

    return {
        "body": json.dumps({
            "statusCode": response_code,
            "message": message})
    }