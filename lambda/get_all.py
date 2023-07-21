import json
import boto3

REGION_NAME = 'YOUR_REGION_NAME'
TABLE_NAME = 'YOUR_TABLE_NAME'

def lambda_handler(event, context):
    # Call the function to get all records from DynamoDB
    response = get_all_records_from_dynamodb()

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def get_all_records_from_dynamodb():
    # Create a Boto3 DynamoDB client
    dynamodb_client = boto3.client('dynamodb', region_name=REGION_NAME)

    try:
        # Perform a scan operation to get all items from the table
        response = dynamodb_client.scan(
            TableName=TABLE_NAME
        )

        # If the scan operation is successful, return the items
        items = response.get('Items', [])
        return items
    except Exception as e:
        # If there's an error, return an error message
        return {"error": str(e)}
