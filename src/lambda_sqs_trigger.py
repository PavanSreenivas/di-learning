import json

def lambda_handler(event, context):
    
    sqs = boto3('sqs')
    queue_name = 'swapistackqueue'
    queue_url = f"https://sqs.us-east-1.amazonaws.com/876332050529/{queue_name}"
    
    request_body = json.loads(event['body'])

    print("Received Movie Data:")
    print(json.dumps(request_body, indent=2))
        
    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(request_body))
    
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Data Received and SQS Message Sent"})
    }
