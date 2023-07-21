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

    # Call the function to delete the record using GSI
    response = delete_record_by_email_from_gsi(email)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def delete_record_by_email_from_gsi(email):
    # Create a Boto3 DynamoDB client
    dynamodb_client = boto3.client('dynamodb', region_name=REGION_NAME)

    try:
        # Query the GSI to get the record with the given email
        response = dynamodb_client.query(
            TableName=TABLE_NAME,
            IndexName=GSI_NAME,
            KeyConditionExpression='email = :val',
            ExpressionAttributeValues={
                ':val': {'S': email}
            }
        )

        # Check if the record was found
        items = response.get('Items', [])
        if len(items) > 0:
            # Delete the record using the UUID (primary key)
            uuid_to_delete = items[0]['uuid']['S']
            dynamodb_client.delete_item(
                TableName=TABLE_NAME,
                Key={
                    'uuid': {'S': uuid_to_delete}
                }
            )
            return {"message": "Record deleted successfully."}
        else:
            return {"message": "Record not found."}

    except Exception as e:
        # If there's an error, return an error message
        return {"error": str(e)}
