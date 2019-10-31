import boto3
import os
import json


# get config.json from s3 bucket.
def get_file():
    s3 = boto3.resource('s3')
    obj = s3.Object(os.getenv('AWS_BUCKET_NAME'), 'config.json')
    body = obj.get()['Body'].read()
    data = json.loads(body)
    return data
