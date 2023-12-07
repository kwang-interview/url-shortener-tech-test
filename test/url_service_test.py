import unittest
import uuid
from unittest import mock
from fastapi import HTTPException

from url_service import UrlService

url_service = UrlService()

# TODO: once clients are refactored, figure out mocking
# class UrlServiceTest(unittest.TestCase):
#     EXPECT_URL = "example.com/" + str(uuid.uuid4())
#
#     @mock.patch("boto3.client")
#     def test_shorten_happy_path(self):
#         short_url = url_service.shorten_url(self.EXPECT_URL)
#         self.assertIsNotNone(short_url)
#
#     def test_shorten_existing(self):
#         short_url = url_service.shorten_url(self.EXPECT_URL)
#         self.assertIsNotNone(short_url)
#
#         short_url_2 = url_service.shorten_url(self.EXPECT_URL)
#         self.assertIsNotNone(short_url_2)
#
#         self.assertEquals(short_url, short_url_2)
#
#     def test_lengthen_path_path(self):
#         short_url = url_service.shorten_url(self.EXPECT_URL)
#         original_url = url_service.lengthen_url(short_url)
#
#         self.assertEquals(self.EXPECT_URL, original_url)
#
#     def test_lengthen_not_found(self):
#         with self.assertRaises(HTTPException):
#             url_service.lengthen_url("not found")
