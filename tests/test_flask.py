from ezproxylookup.views import get_json_file
import os


def test_get_json_file_from_s3(s3_conn):
    os.environ['CONFIG_FILE_LOCATION'] = "aws-s3"
    f = get_json_file()
    assert f[0]['title'] == 'A Title'


def test_get_json_file_from_local_default():
    """ uses default local file when no location is given """
    del os.environ['CONFIG_FILE_LOCATION']
    f = get_json_file()
    assert f[0]['title'] == 'included fake title number one'


def test_get_json_file_from_local_specified():
    """ uses the local file specified in ENV """
    os.environ['CONFIG_FILE_LOCATION'] = "tests\
/fixtures/other_fake_config.json"
    f = get_json_file()
    assert f[0]['title'] == 'other fake config file'


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


def test_route_econtrol(client, s3_conn):
    """ econtrol returns 200 """
    response = client.get('/econtrol')
    assert response.status_code == 200


def test_route_bad_route(client):
    """ returns 404 with bad route"""
    response = client.get('/not_a_route')
    assert response.status_code == 404
