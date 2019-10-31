import ezproxylookup
import boto3
from moto import mock_s3
import pytest


@pytest.fixture
def fake_config_json():
    config_json = """

        [{
        "title": "A Title",
        "config_file": "fake_config_file.txt",
        "urls": ["http://example.com"]
        }]
        """
    return config_json


@pytest.fixture(autouse=True)
def aws_credentials(monkeypatch):
    monkeypatch.setenv('AWS_BUCKET', 'samples')


@pytest.yield_fixture
def app():
    app = ezproxylookup.app
    ctx = app.test_request_context()
    ctx.push()
    yield app
    ctx.pop()


@pytest.fixture
def client(app):
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost'
    client = app.test_client()
    return client


@pytest.fixture(autouse=True)
def s3_conn(fake_config_json):
    with mock_s3():
        conn = boto3.resource('s3', region_name='us-east-1')
        conn.create_bucket(Bucket='samples')
        # config.json must be an array of dicts, otherwise /econfig won't work
        # (for example, a single dict will cause it to fail)
        conn.Object('samples', 'config.json').put(Body=fake_config_json)
        yield conn
