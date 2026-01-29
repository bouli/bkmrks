from bkmrks import urls
import pytest

def test_ensure_domain():
    assert "https://domain.com" == urls.ensure_domain(url="",domain="https://domain.com")
    assert "https://domain.com/" == urls.ensure_domain(url="/",domain="https://domain.com")

    assert "https://domain.com?param=1" == urls.ensure_domain(url="?param=1",domain="https://domain.com")
    assert "https://domain.com/?param=1" == urls.ensure_domain(url="/?param=1",domain="https://domain.com")

    assert "https://domain.com#anchor" == urls.ensure_domain(url="#anchor",domain="https://domain.com")
    assert "https://domain.com/#anchor" == urls.ensure_domain(url="/#anchor",domain="https://domain.com")

    assert "https://domain.com/path" == urls.ensure_domain(url="path",domain="https://domain.com")
    assert "https://domain.com/path" == urls.ensure_domain(url="/path",domain="https://domain.com")
    assert "https://domain.com/path" == urls.ensure_domain(url="/path",domain="http://domain.com")

    assert "https://domain.com/path" == urls.ensure_domain(url="https://domain.com/path",domain="https://otherdomain.com")
    assert "https://domain.com/path" == urls.ensure_domain(url="http://domain.com/path",domain="https://domain.com")
    assert "https://domain.com/path" == urls.ensure_domain(url="http://domain.com/path",domain="")

    assert "https://domain.com/path" == urls.ensure_domain(url="/path",domain="https://domain.com/other-path")

    with pytest.raises(TypeError):
        urls.ensure_domain(url="/path")

    with pytest.raises(ValueError):
        urls.ensure_domain(url="/path",domain="not-a-domain.com")

def test_get_name_by_url():
    with pytest.raises(TypeError):
        urls.get_name_by_url()
    with pytest.raises(ValueError):
        urls.get_name_by_url(url="testing.com.br")
    assert "testing" == urls.get_name_by_url(url="http://www.testing.com.br")
    assert "testing" == urls.get_name_by_url(url="http://testing.com.br")
    assert "testing" == urls.get_name_by_url(url="http://testing.com")
    assert "google_gservice" == urls.get_name_by_url(url="http://gservice.google.com")
    assert "google_gservice" == urls.get_name_by_url(url="http://subdomain.gservice.google.com")

def test_extract_domain_from_url():
    with pytest.raises(TypeError):
        urls.extract_domain_from_url()

    assert "http://www.testing.com.br" == urls.extract_domain_from_url(url="http://www.testing.com.br")
    assert "http://www.testing.com.br" == urls.extract_domain_from_url(url="http://www.testing.com.br/path?param1#anchor")
    assert "" == urls.extract_domain_from_url(url="www.testing.com.br")
    assert "" == urls.extract_domain_from_url(url="/asdf")

def test_read_from_url_or_path():
    return
