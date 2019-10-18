
import pytest
from ezproxylookup import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = 'localhost'
    client = app.test_client()
    return client


def test_route_get(client):
    response = client.get('/')
    assert response.status_code == 200


def test_route_empty_post(client):
    """ post with no data is redirected """
    response = client.post('/')
    assert response.status_code == 302


def test_route_post_form_data(client):
    """ post with form data is 200 """
    response = client.post('/',
                           data={'url': 'jstor.org'},
                           headers={'Accept': 'text/html'})
    assert response.status_code == 200


def test_route_post_json_data(client):
    """ post with data and accpet header = application/json returns json

        search term is returned in json response
    """
    search_term = "jstor.org"
    response = client.post('/',
                           data={'url': search_term},
                           headers={'Accept': 'application/json'})
    assert response.status_code == 200
    assert response.is_json
    assert response.get_json()['search_term'] == search_term


def test_route_econtrol(client):
    """ econtrol returns 200 """
    response = client.get('/econtrol')
    assert response.status_code == 200


def test_route_bad_route(client):
    """ returns 404 with bad route"""
    response = client.get('/not_a_route')
    assert response.status_code == 404
