import boto3

# TODO: configs to yaml or some other env based support
CLIENT_NAME = 'dynamodb'
REGION_NAME = 'local'
ENDPOINT_URL = 'http://dynamodb-local:9000'
ACCESS_KEY = 'access'
SECRET_KEY = 'secret'
SESSION_TOKEN = 'token'

# table names
URL_MAPPING_TABLE = 'UrlMappingTable'


class DynamoClient:
    client = boto3.client(
        CLIENT_NAME,
        region_name=REGION_NAME,
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN
    )
