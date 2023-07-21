import json
import boto3
import uuid

REGION_NAME = 'YOUR_REGION_NAME'
TABLE_NAME = 'YOUR_TABLE_NAME'

def lambda_handler(event, context):
    # Parse the incoming JSON event containing data to be inserted
    try:
        data = json.loads(event['body'])
    except ValueError:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid JSON payload.')
        }

    # Generate a UUID for the record
    data['uuid'] = str(uuid.uuid4())

    # Call the function to insert data into DynamoDB
    response = insert_data_into_dynamodb(data)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def insert_data_into_dynamodb(data):
    # Create a Boto3 DynamoDB client
    dynamodb_client = boto3.client('dynamodb', region_name=REGION_NAME)

    try:
        # Insert data into DynamoDB
        response = dynamodb_client.put_item(
            TableName=TABLE_NAME,
            Item=data
        )

        # If successful, return the inserted data
        return response
    except Exception as e:
        # If there's an error, return an error message
        return {"error": str(e)}
