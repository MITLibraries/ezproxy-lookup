
import pytest
from ezproxylookup import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost'
    client = app.test_client()
    return client


def test_views_get(client):
    response = client.get('/')
    assert response.status_code == 200


def test_view_post_empty(client):
    """ post with no data is redirected """
    response = client.post('/')
    assert response.status_code == 302
