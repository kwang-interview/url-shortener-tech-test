from typing import Any

import boto3
from botocore.client import BaseClient

# TODO: configs to yaml or some other env based support
CLIENT_NAME = 'dynamodb'
REGION_NAME = 'local'
ENDPOINT_URL = 'http://dynamodb-local:9000'
ACCESS_KEY = 'access'
SECRET_KEY = 'secret'
SESSION_TOKEN = 'token'

# table names
URL_MAPPING_TABLE = 'UrlMappingTable'

default_client = boto3.client(
    CLIENT_NAME,
    region_name=REGION_NAME,
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN
)

default_resource = boto3.resource(
    CLIENT_NAME,
    region_name=REGION_NAME,
    endpoint_url=ENDPOINT_URL,
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN
)
default_table = default_resource.Table(URL_MAPPING_TABLE)


class DynamoClient:
    client: BaseClient

    def __init__(self, dynamo_client: BaseClient = default_client):
        self.client = dynamo_client


class TableClient:
    url_mapping: Any

    def __init__(self, url_mapping_table=default_table):
        self.url_mapping = url_mapping_table
