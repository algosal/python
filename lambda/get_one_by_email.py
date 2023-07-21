import json
import boto3

REGION_NAME = 'YOUR_REGION_NAME'
TABLE_NAME = 'YOUR_TABLE_NAME'

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

    # Call the function to get the record from DynamoDB
    response = get_record_from_dynamodb(email)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def get_record_from_dynamodb(email):
    # Create a Boto3 DynamoDB client
    dynamodb_client = boto3.client('dynamodb', region_name=REGION_NAME)

    try:
        # Get the record from DynamoDB using the email as the key
        response = dynamodb_client.get_item(
            TableName=TABLE_NAME,
            Key={
                'email': {'S': email}
            }
        )

        # If the record is found, return it; otherwise, return a message
        item = response.get('Item')
        if item:
            return item
        else:
            return {"message": "Record not found."}
    except Exception as e:
        # If there's an error, return an error message
        return {"error": str(e)}
