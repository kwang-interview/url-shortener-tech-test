import boto3

import const
from logger import get_logger

logger = get_logger(__name__)

logger.info("Running migration...")
# TODO: move clients to standalone then have other classes reference it
# TODO: configs to yaml
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
                'AttributeName': const.URL_ID,
                'AttributeType': 'S',
            },
            {
                'AttributeName': const.URL,
                'AttributeType': 'S',
            },
        ],
        KeySchema=[
            {
                'AttributeName': const.URL_ID,
                'KeyType': 'HASH',
            }
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'urlIdx',
                'KeySchema': [
                    {
                        'AttributeName': const.URL,
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
