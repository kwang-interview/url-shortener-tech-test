from logger import get_logger
import boto3

table_name: str = "UrlMappingTable"
dynamodb = boto3.resource(
    'dynamodb',
    region_name='local',
    endpoint_url="http://dynamodb-local:8000",
    aws_access_key_id='access',
    aws_secret_access_key='secret',
    aws_session_token='token'
)
table = dynamodb.Table(table_name)

logger = get_logger(__name__)


class UrlService:
    def __init__(self):
        pass

    @staticmethod
    def shorten_url(original_url: str) -> str:
        logger.info("shortening...")

        return original_url

    @staticmethod
    def lengthen_url(short_url: str) -> str:
        logger.info("lengthening...")

        return short_url
