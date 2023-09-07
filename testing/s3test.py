import os
import json
import boto3
import pandas as pd
from io import StringIO

def lambda_handler(event, context):
    s3_event = event['Records'][0]['s3']
    bucket_name = s3_event['bucket']['name']
    object_key = s3_event['object']['key']
    
    # Extract the file name from the object key
    file_name = object_key.split('/')[-1]
    
    # Check if the uploaded/modified object is a CSV file
    if file_name.endswith('.csv'):
        # Initialize an S3 client
        s3_client = boto3.client('s3')
    
        # Get the CSV file content from S3
        s3_response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        csv_data = s3_response["Body"].read().decode('utf-8')
        
        # Create a DataFrame from CSV content using pandas
        df = pd.read_csv(StringIO(csv_data))
        
        # Print the first 5 rows
        print(f"First 5 rows from CSV file {file_name} in s3://{bucket_name}/{object_key}:")
        print(df.head())
    else:
        print(f"Non-CSV file {file_name} uploaded/modified: s3://{bucket_name}/{object_key}")
