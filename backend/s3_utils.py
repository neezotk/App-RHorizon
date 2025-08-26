import boto3
from botocore.exceptions import BotoCoreError, ClientError
from .config import settings

s3 = boto3.client("s3", region_name=settings.AWS_REGION)

def s3_healthcheck():
    try:
        if not settings.S3_BUCKET_NAME:
            return False, "S3_BUCKET_NAME is not set"
        s3.head_bucket(Bucket=settings.S3_BUCKET_NAME)
        return True, None
    except (BotoCoreError, ClientError) as e:
        return False, str(e)

def upload_fileobj(fileobj, key: str, content_type: str = "application/octet-stream"):
    extra_args = {"ContentType": content_type}
    s3.upload_fileobj(fileobj, settings.S3_BUCKET_NAME, key, ExtraArgs=extra_args)
    return {"bucket": settings.S3_BUCKET_NAME, "key": key, "url": f"s3://{settings.S3_BUCKET_NAME}/{key}"}
