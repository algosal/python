import json
import boto3

REGION_NAME = 'YOUR_REGION_NAME'
TABLE_NAME = 'YOUR_TABLE_NAME'

def lambda_handler(event, context):
    # Parse the incoming JSON event containing the UUID and updated data
    try:
        data = json.loads(event['body'])
        uuid_to_update = data.get('uuid')
        if not uuid_to_update:
            raise ValueError("UUID field is missing.")
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }

    # Remove the UUID from the data as we don't want to update the primary key
    del data['uuid']

    # Call the function to update the record using the UUID and updated data
    response = update_record_by_uuid(uuid_to_update, data)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def update_record_by_uuid(uuid_to_update, updated_data):
    # Create a Boto3 DynamoDB client
    dynamodb_client = boto3.client('dynamodb', region_name=REGION_NAME)

    try:
        # Update the record using the UUID (primary key) and updated data
        response = dynamodb_client.update_item(
            TableName=TABLE_NAME,
            Key={
                'uuid': {'S': uuid_to_update}
            },
            UpdateExpression='SET ' + ', '.join(f'#{k} = :{k}' for k in updated_data.keys()),
            ExpressionAttributeNames={f'#{k}': k for k in updated_data.keys()},
            ExpressionAttributeValues={f':{k}': {data_type(updated_data[k]): updated_data[k]} for k in updated_data.keys()},
            ReturnValues='ALL_NEW'
        )

        # If the update is successful, return the updated record
        item = response.get('Attributes')
        return item

    except Exception as e:
        # If there's an error, return an error message
        return {"error": str(e)}

def data_type(value):
    # Helper function to determine the data type of the attribute
    if isinstance(value, int):
        return 'N'
    elif isinstance(value, float):
        return 'N'
    elif isinstance(value, str):
        return 'S'
    elif isinstance(value, list):
        return 'L'
    elif isinstance(value, dict):
        return 'M'
    else:
        raise ValueError("Unsupported data type.")
