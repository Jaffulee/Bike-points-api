from datetime import datetime
# import datetime
import json
import time
import os
from dotenv import load_dotenv
import requests as rq
from botocore.exceptions import ClientError
import boto3

def load_bike_json():
    load_dotenv()

    filepath_base = 'data'
    filenames = os.listdir(filepath_base)
    # filenames = [f for f in filenames if f.endswith('.json') and filenames]
    print(filenames)
    s3filepath_base = 'bike-point'

    api_keys = {'Access_key_ID' : os.getenv('Access_key_ID'),
    'Secret_access_key' : os.getenv('Secret_access_key'),
    'AWS_BUCKET_NAME' : os.getenv('AWS_BUCKET_NAME')}
    print(api_keys)

    s3_client = boto3.client(
        's3',
        aws_access_key_id = api_keys['Access_key_ID'],
        aws_secret_access_key = api_keys['Secret_access_key'],
        region_name = 'eu-north-1'
    )
    for filename in filenames:
        try:
            # filepath = os.path.join(filepath_base,filename)
            # s3_path = os.path.join(s3filepath_base,filename)
            filepath = filepath_base + '/' + filename
            s3_path = s3filepath_base + '/' + filename
            print(filepath,s3_path)
            s3_client.upload_file(
                Filename=filepath,   # local path
                Bucket=api_keys['AWS_BUCKET_NAME'],             # target bucket
                Key=s3_path,# object key (path in bucket)
            )
            os.remove(filepath)
            print("Upload succeeded")
        except ClientError as err:
            print(f"Upload failed: {err}")


    print(s3_client)
    return

if __name__ == '__main__':
    load_bike_json()
