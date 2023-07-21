import boto3

# Replace these values with your AWS credentials and DynamoDB table information
AWS_ACCESS_KEY_ID = 'YOUR_ACCESS_KEY_ID'
AWS_SECRET_ACCESS_KEY = 'YOUR_SECRET_ACCESS_KEY'
REGION_NAME = 'YOUR_REGION_NAME'
TABLE_NAME = 'YOUR_TABLE_NAME'

def insert_data_into_dynamodb(data):
    # Create a Boto3 DynamoDB client
    dynamodb_client = boto3.client('dynamodb', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION_NAME)

    try:
        # Insert data into DynamoDB
        response = dynamodb_client.put_item(
            TableName=TABLE_NAME,
            Item=data
        )

        # If successful, response contains the inserted data
        print("Data inserted successfully:", response)
    except Exception as e:
        print("Error inserting data:", e)

if __name__ == "__main__":
    # Example data to insert into DynamoDB
    example_data = {
        'id': {'S': '1'},
        'name': {'S': 'John Doe'},
        'age': {'N': '30'},
        # Add other attributes as needed
    }

    insert_data_into_dynamodb(example_data)
