import boto3
from logger import get_logger

logger = get_logger(__name__)

logger.info("Running migration...")
dynamodb_client = boto3.client(
    'dynamodb',
    region_name='local',
    endpoint_url="http://dynamodb-local:9000",
    aws_access_key_id='access',
    aws_secret_access_key='secret',
    aws_session_token='token'
)

try:
    response = dynamodb_client.create_table(
        AttributeDefinitions=[
            {
                'AttributeName': 'urlId',
                'AttributeType': 'S',
            },
            {
                'AttributeName': 'url',
                'AttributeType': 'S',
            },
        ],
        KeySchema=[
            {
                'AttributeName': 'urlId',
                'KeyType': 'HASH',
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'urlIdx',
                'KeySchema': [
                    {
                        'AttributeName': 'url',
                        'KeyType': 'HASH'
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5,
                }
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5,
        },
        TableName='UrlMappingTable',
    )
except dynamodb_client.exceptions.ResourceInUseException:
    pass

logger.info("Migration completed")
