import const
from dynamo_client import DynamoClient, URL_MAPPING_TABLE
from logger import get_logger

logger = get_logger(__name__)


class Migration:
    dynamo_client: DynamoClient

    def __init__(self, dynamo_client: DynamoClient):
        self.dynamo_client = dynamo_client

    def migrate(self):
        logger.info("Running migration...")
        try:
            response = self.dynamo_client.client.create_table(
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
                TableName=URL_MAPPING_TABLE,
            )
        except self.dynamo_client.client.exceptions.ResourceInUseException:
            pass

        logger.info("Migration completed")
