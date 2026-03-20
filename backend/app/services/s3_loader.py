import boto3
import os

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    region_name=AWS_REGION,
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def download_s3_file(key: str, local_path: str):

    os.makedirs(os.path.dirname(local_path), exist_ok=True)

    s3.download_file(S3_BUCKET, key, local_path)

    return local_path
