import json
import boto3
import csv

def lambda_handler(event, context):
    s3_event = event['Records'][0]['s3']
    bucket = s3_event['bucket']['name']
    object_key = s3_event['object']['key']
    
    # Check if the uploaded/modified object is a CSV file
    if object_key.endswith('.csv'):
        # Initialize an S3 client
        s3_client = boto3.client('s3')
        
        # Get the CSV file content from S3
        response = s3_client.get_object(Bucket=bucket, Key=object_key)
        csv_content = response['Body'].read().decode('utf-8')
        
        # Parse CSV content
        csv_rows = csv_content.split('\n')
        
        # Print the first 5 rows
        print(f"First 5 rows from CSV file s3://{bucket}/{object_key}:")
        for i, row in enumerate(csv.reader(csv_rows)):
            if i < 5:
                print(row)
            else:
                break
    else:
        print(f"Non-CSV file uploaded/modified: s3://{bucket}/{object_key}")

        