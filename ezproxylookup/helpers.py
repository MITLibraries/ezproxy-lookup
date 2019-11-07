import boto3
import os
import json


def get_json_file():
    if os.getenv('CONFIG_FILE_LOCATION') == "aws-s3":
        s3 = boto3.resource('s3')
        obj = s3.Object(os.getenv('AWS_BUCKET_NAME'), 'config.json')
        body = obj.get()['Body'].read()
        data = json.loads(body)
    else:
        # If a local config.json file is specified, use it.
        # otherwise use the default local config.json file.

        local_config_json = os.getenv('CONFIG_FILE_LOCATION',
                                      os.path.join('tests', 'fixtures',
                                                   'fake_config.json'))
        with open(local_config_json) as f:
            data = json.loads(f.read())
    return data
