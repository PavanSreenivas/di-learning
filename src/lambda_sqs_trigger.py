import boto3
import json

def lambda_handler(event, context):
    
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/876332050529/swapistackqueue'
    
    data = json.loads(event['body'])
    
    message = json.dumps(data)
    print(data)
    
    response = sqs.send_message(QueueUrl=queue_url,MessageBody = message)
    
    response_code = response["ResponseMetadata"]["HTTPStatusCode"]
    
    return {
        "body": json.dumps({
            "statusCode": response_code,
            "message": "Data Received and SQS Message Sent"})
    }
