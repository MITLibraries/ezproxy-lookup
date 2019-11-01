import boto3
import os
import json
from ezproxylookup import app


# get config.json from s3 bucket.
def get_file():
    if app.config['ENV'] == 'development':
        with open(os.getenv('DEV_CONFIG_JSON')) as f:
            data = json.loads(f.read())
    else:
        s3 = boto3.resource('s3')
        obj = s3.Object(os.getenv('AWS_BUCKET_NAME'), 'config.json')
        body = obj.get()['Body'].read()
        data = json.loads(body)
    return data
