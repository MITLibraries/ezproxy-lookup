import utilities.config_to_json as config_to_json
import pytest
import os
from click.testing import CliRunner
import filecmp

current_dir = os.path.dirname(os.path.realpath(__file__))
fake_config_file = os.path.join(current_dir, 'fixtures',
                                'fake_config_file.txt')
test_outfile = os.path.join(current_dir, 'fixtures',
                            'fake_config.json')


with open(fake_config_file) as f:
    base_config_file_text = f.read()


@pytest.fixture
def config_results():
    config_data = {
        "config_file": fake_config_file,
        "content": config_to_json.get_config_contents(fake_config_file)
                  }
    config_results = config_to_json.get_stanzas(config_data)
    return config_results


def test_get_included_files():
    results = config_to_json.get_included_files(base_config_file_text)
    assert "included_fake_config.txt" in results


def test_get_config_contents():
    results = config_to_json.get_config_contents(fake_config_file)
    assert any(["http://fake.url" in s for s in results])


def test_get_config_contents_missing_file():
    results = config_to_json.get_config_contents('missing_config.txt')
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
    x = config_to_json.filter_stanzas(config_results)
    assert len(config_results) == 4
    assert len(x) == 3


def test_click():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(config_to_json.parse,
                               ['--infile', f'{fake_config_file}',
                                '--outfile', 'test_out.json'])
        assert filecmp.cmp('test_out.json', test_outfile, shallow=False)
        assert result.exit_code == 0
