import uuid
from typing import Any

from boto3.dynamodb.conditions import Key
from fastapi import HTTPException

import const
from dynamo_client import DynamoClient
from logger import get_logger

logger = get_logger(__name__)


# TODO: switch to interfaced usage
class UrlService:
    table: Any

    def __init__(self, dynamo_client: DynamoClient):
        table_name: str = "UrlMappingTable"
        self.table = dynamo_client.client.Table(table_name)

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

    def get_id_from_db(self, url: str) -> str:
        # query always return list
        response = self.table.query(
            IndexName='urlIdx',
            KeyConditionExpression=Key(const.URL).eq(url)
        )
        url_list = response.get("Items")

        if len(url_list) == 0:
            raise HTTPException(status_code=404, detail="Url not found")

        return url_list[0].get(const.URL_ID)

    def get_url_from_db(self, url_id: str) -> str:
        # get always return one
        response = self.table.get_item(Key={const.URL_ID: url_id})
        url = response.get("Item")

        if not url:
            raise HTTPException(status_code=404, detail="Url not found")

        return url.get(const.URL)

    def save_url_to_db(self, url_id: str, url: str):
        self.table.put_item(
            Item={
                const.URL_ID: url_id,
                const.URL: url,
            }
        )
