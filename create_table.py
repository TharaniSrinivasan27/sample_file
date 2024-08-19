import boto3
import config    # Import your config file

def create_dynamodb_table():
    # Create the DynamoDB service resource using credentials from config.py
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=config.AWS_REGION,
        aws_access_key_id=config.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY
    )

    # Define the table schema
    table = dynamodb.create_table(
        TableName=config.TABLE_NAME,
        KeySchema=[
            {
                'AttributeName': 'primaryid',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'mail',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'primaryid',
                'AttributeType': 'S'  # 'S' for string, 'N' for number, 'B' for binary
            },
            {
                'AttributeName': 'mail',
                'AttributeType': 'S'  # 'S' for string, 'N' for number, 'B' for binary
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )

    # Wait until the table exists
    table.meta.client.get_waiter('table_exists').wait(TableName=config.TABLE_NAME)

    print(f"Table {table.table_name} created successfully!")

if __name__ == '__main__':
    create_dynamodb_table()
