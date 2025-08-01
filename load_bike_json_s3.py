"""
Module to upload JSON files from a local directory to an S3 bucket.

This script reads JSON files from the `data/` directory, uploads them to
a specified AWS S3 bucket, and deletes the local file upon successful upload.
Environment variables must be defined in a `.env` file.
"""

import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError


def load_bike_json():
    """
    Loads all `.json` files from the `data/` directory and uploads them
    to an AWS S3 bucket. After a successful upload, the local file is deleted.
    
    Environment variables expected (in a `.env` file):
        - Access_key_ID
        - Secret_access_key
        - AWS_BUCKET_NAME
    """
    load_dotenv()

    # Local and S3 paths
    local_dir = 'data'
    s3_dir = 'bike-point'

    # Read local file names
    filenames = os.listdir(local_dir)
    print(f"Files found: {filenames}")

    # Load AWS credentials from environment
    aws_credentials = {
        'aws_access_key_id': os.getenv('Access_key_ID'),
        'aws_secret_access_key': os.getenv('Secret_access_key'),
        'bucket_name': os.getenv('AWS_BUCKET_NAME')
    }
    print(f"AWS Credentials Loaded: {aws_credentials}")

    # Initialize S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_credentials['aws_access_key_id'],
        aws_secret_access_key=aws_credentials['aws_secret_access_key'],
        region_name='eu-north-1'
    )

    # Upload each .json file to S3
    for filename in filenames:
        if filename.endswith('.json'):
            local_path = os.path.join(local_dir, filename)
            s3_path = s3_dir + '/' + filename


            try:
                s3_client.upload_file(
                    Filename=local_path,
                    Bucket=aws_credentials['bucket_name'],
                    Key=s3_path
                )
                os.remove(local_path)
                print(f"✅ Uploaded and removed local file: {filename}")
            except ClientError as err:
                print(f"❌ Upload failed for {filename}: {err}")

    return


if __name__ == '__main__':
    load_bike_json()
