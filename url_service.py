from boto3.dynamodb.conditions import Key
from fastapi import HTTPException

import const
from logger import get_logger
import boto3
import uuid

table_name: str = "UrlMappingTable"
dynamodb = boto3.resource(
    'dynamodb',
    region_name='local',
    endpoint_url="http://dynamodb-local:9000",
    aws_access_key_id='access',
    aws_secret_access_key='secret',
    aws_session_token='token'
)
table = dynamodb.Table(table_name)

logger = get_logger(__name__)


# TODO: switch to interfaced usage
class UrlService:
    def __init__(self):
        pass

    def shorten_url(self, original_url: str) -> str:
        logger.debug("shortening...")
        try:
            # url has already been shortened, returning existing short path
            return self.get_id_from_db(original_url)
        except Exception:
            pass

        new_url_id = str(uuid.uuid4())
        self.save_url_to_db(new_url_id, original_url)

        return new_url_id

    def lengthen_url(self, short_url: str) -> str:
        logger.debug("lengthening...")
        return self.get_url_from_db(short_url)

    @staticmethod
    def get_id_from_db(url: str) -> str:
        # query always return list
        response = table.query(
            IndexName='urlIdx',
            KeyConditionExpression=Key(const.URL).eq(url)
        )
        url_list = response.get("Items")

        if len(url_list) == 0:
            raise HTTPException(status_code=404, detail="Url not found")

        return url_list[0].get(const.URL_ID)

    @staticmethod
    def get_url_from_db(url_id: str) -> str:
        # get always return one
        response = table.get_item(Key={const.URL_ID: url_id})
        url = response.get("Item")

        if not url:
            raise HTTPException(status_code=404, detail="Url not found")

        return url.get(const.URL)

    @staticmethod
    def save_url_to_db(url_id: str, url: str):
        table.put_item(
            Item={
                const.URL_ID: url_id,
                const.URL: url,
            }
        )
