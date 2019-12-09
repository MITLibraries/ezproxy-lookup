from utilities.config_to_json import (get_included_files, get_config_contents,
                                      get_stanzas, filter_stanzas)
import pytest
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
fake_config_file = os.path.join(current_dir, 'fixtures',
                                'fake_config_file.txt')

with open(fake_config_file) as f:
    base_config_file_text = f.read()


@pytest.fixture
def config_results():
    config_data = {
        "config_file": fake_config_file,
        "content": get_config_contents(fake_config_file)
                  }
    config_results = get_stanzas(config_data)
    return config_results


def test_get_included_files():
    results = get_included_files(base_config_file_text)
    assert "included_fake_config.txt" in results


def test_get_config_contents():
    results = get_config_contents(fake_config_file)
    assert any(["http://fake.url" in s for s in results])


def test_get_config_contents_missing_file():
    results = get_config_contents('missing_config.txt')
    assert results == ''


def test_get_stanzas(config_results):
    url_param = "password=my_secret"
    url_list = [item for urls in (stanza['urls'] for stanza in config_results)
                for item in urls]
    assert not any([url_param in s for s in url_list])
    assert any(['http://fake.url-number.three' in s for s in url_list])


def test_get_stanzas_keys(config_results):
    """get_stanzas list contains only title, urls, and config_file keys """
    keys = set().union(*(d.keys()for d in config_results))
    assert {'urls', 'title', 'config_file'} == keys


def test_filter_stanzas(config_results):
    """filter_stanazas removes stanzas with a -hide flag in the
    title directive"""
    x = filter_stanzas(config_results)
    assert len(config_results) == 4
    assert len(x) == 3
