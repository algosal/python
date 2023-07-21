import json
import boto3

REGION_NAME = 'YOUR_REGION_NAME'
TABLE_NAME = 'YOUR_TABLE_NAME'
GSI_NAME = 'EmailIndex'

def lambda_handler(event, context):
    # Parse the incoming JSON event containing the email
    try:
        data = json.loads(event['body'])
        email = data.get('email')
        if not email:
            raise ValueError("Email field is missing.")
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }

    # Call the function to get all records with the given email from the GSI
    response = get_records_by_email_from_gsi(email)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def get_records_by_email_from_gsi(email):
    # Create a Boto3 DynamoDB client
    dynamodb_client = boto3.client('dynamodb', region_name=REGION_NAME)

    try:
        # Query the GSI to get all items with the given email
        response = dynamodb_client.query(
            TableName=TABLE_NAME,
            IndexName=GSI_NAME,
            KeyConditionExpression='email = :val',
            ExpressionAttributeValues={
                ':val': {'S': email}
            }
        )

        # If the query is successful, return the items
        items = response.get('Items', [])
        return items
    except Exception as e:
        # If there's an error, return an error message
        return {"error": str(e)}
