import json
import boto3

REGION_NAME = 'YOUR_REGION_NAME'
TABLE_NAME = 'YOUR_TABLE_NAME'

def lambda_handler(event, context):
    # Parse the incoming JSON event containing the UUID
    try:
        data = json.loads(event['body'])
        uuid_to_delete = data.get('uuid')
        if not uuid_to_delete:
            raise ValueError("UUID field is missing.")
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }

    # Call the function to delete the record using the UUID
    response = delete_record_by_uuid(uuid_to_delete)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def delete_record_by_uuid(uuid_to_delete):
    # Create a Boto3 DynamoDB client
    dynamodb_client = boto3.client('dynamodb', region_name=REGION_NAME)

    try:
        # Delete the record using the UUID (primary key)
        dynamodb_client.delete_item(
            TableName=TABLE_NAME,
            Key={
                'uuid': {'S': uuid_to_delete}
            }
        )
        return {"message": "Record deleted successfully."}

    except Exception as e:
        # If there's an error, return an error message
        return {"error": str(e)}
