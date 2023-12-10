import unittest
import uuid

import boto3
import moto
from fastapi import HTTPException

from db_migration import Migration
from dynamo_client import DynamoClient, URL_MAPPING_TABLE, TableClient, CLIENT_NAME
from url_service import UrlService


@moto.mock_dynamodb
class UrlServiceTest(unittest.TestCase):
    EXPECT_URL = "example.com/" + str(uuid.uuid4())
    url_service: UrlService

    def setUp(self):
        dynamo_client = DynamoClient(boto3.client(CLIENT_NAME, 'us-east-1'))
        Migration(dynamo_client).migrate()

        dynamodb = boto3.resource(CLIENT_NAME, 'us-east-1')
        table = dynamodb.Table(URL_MAPPING_TABLE)

        self.url_service = UrlService(TableClient(table))

    def test_shorten_happy_path(self):
        short_url = self.url_service.shorten_url(self.EXPECT_URL)
        self.assertIsNotNone(short_url)

    def test_shorten_existing(self):
        short_url = self.url_service.shorten_url(self.EXPECT_URL)
        self.assertIsNotNone(short_url)

        short_url_2 = self.url_service.shorten_url(self.EXPECT_URL)
        self.assertIsNotNone(short_url_2)

        self.assertEquals(short_url, short_url_2)

    def test_lengthen_path_path(self):
        short_url = self.url_service.shorten_url(self.EXPECT_URL)
        original_url = self.url_service.lengthen_url(short_url)

        self.assertEquals(self.EXPECT_URL, original_url)

    def test_lengthen_not_found(self):
        with self.assertRaises(HTTPException):
            self.url_service.lengthen_url("not found")
