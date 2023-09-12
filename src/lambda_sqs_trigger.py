import boto3
import json

sqs = boto3.client('sqs')
queue_name = 'swapistackqueue'    
queue_url = f"https://sqs.us-east-1.amazonaws.com/876332050529/{queue_name}"

def lambda_handler(event, context):
    
    data = json.loads(event['body'])

    print("Received Movie Data:")
    print(json.dumps(data, indent=2))
        
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(data))
    
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Data Received and SQS Message Sent"})
    }
