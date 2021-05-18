import boto3
from config import Config
import requests

s3 = boto3.client(
    's3',
    aws_access_key_id=Config.AWS_ACCESS_KEY,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    region_name='eu-south-1',
    endpoint_url='https://s3.eu-south-1.amazonaws.com'
)

S3_LOCATION = f'http://{Config.BUCKET_NAME}.s3.eu-south-1.amazonaws.com/'