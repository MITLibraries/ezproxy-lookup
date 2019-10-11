from utilities.config_to_json import parse_config
from pathlib import Path
import pytest

fake_config_file = Path(__file__).with_name("fake_config_file.txt")


@pytest.fixture
def config_results():
    results = parse_config(Path(fake_config_file))
    return results


def test_parse_config_type(config_results):
    """ the result of running parse_config is a list """
    assert type(config_results) is list


def test_parse_config_length(config_results):
    """ parse_config returns a list with more than 0 items """
    assert len(config_results) > 0


def test_parse_config_keys(config_results):
    """parse_config list contains only title, urls, and config_file keys """
    keys = set().union(*(d.keys()for d in config_results))
    assert {'urls', 'title', 'config_file'} == keys


def test_parse_config_scrub_url_params(config_results):
    """ parse_config scrubs url params """
    url_param = "password=my_secret"
    url_list = [item for urls in (stanza['urls'] for stanza in config_results)
                for item in urls]
    assert not any([url_param in s for s in url_list])
    assert any(['http://fake.url-number.three' in s for s in url_list])


def test_parse_config_included_file(config_results):
    """ parse_config handles included files """
    url = "http://included.fake.url-number.two"
    url_list = [item for urls in (stanza['urls'] for stanza in config_results)
                for item in urls]
    assert any([url in s for s in url_list])
