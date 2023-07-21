import json
import boto3

REGION_NAME = 'YOUR_REGION_NAME'
TABLE_NAME = 'YOUR_TABLE_NAME'
GSI_NAME = 'EmailIndex'

def lambda_handler(event, context):
    # Parse the incoming JSON event containing the email and updated data
    try:
        data = json.loads(event['body'])
        email_to_update = data.get('email')
        if not email_to_update:
            raise ValueError("Email field is missing.")
    except ValueError as e:
        return {
            'statusCode': 400,
            'body': json.dumps(str(e))
        }

    # Remove the email from the data as we don't want to update the GSI key
    del data['email']

    # Call the function to update the record using the GSI and updated data
    response = update_record_by_email_from_gsi(email_to_update, data)

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def update_record_by_email_from_gsi(email_to_update, updated_data):
    # Create a Boto3 DynamoDB client
    dynamodb_client = boto3.client('dynamodb', region_name=REGION_NAME)

    try:
        # Query the GSI to get the record with the given email
        response = dynamodb_client.query(
            TableName=TABLE_NAME,
            IndexName=GSI_NAME,
            KeyConditionExpression='email = :val',
            ExpressionAttributeValues={
                ':val': {'S': email_to_update}
            }
        )

        # Check if the record was found
        items = response.get('Items', [])
        if len(items) > 0:
            # Get the UUID of the record to update
            uuid_to_update = items[0]['uuid']['S']

            # Update the record using the UUID (primary key) and updated data
            dynamodb_client.update_item(
                TableName=TABLE_NAME,
                Key={
                    'uuid': {'S': uuid_to_update}
                },
                UpdateExpression='SET ' + ', '.join(f'#{k} = :{k}' for k in updated_data.keys()),
                ExpressionAttributeNames={f'#{k}': k for k in updated_data.keys()},
                ExpressionAttributeValues={f':{k}': {data_type(updated_data[k]): updated_data[k]} for k in updated_data.keys()},
            )

            return {"message": "Record updated successfully."}
        else:
            return {"message": "Record not found."}

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
