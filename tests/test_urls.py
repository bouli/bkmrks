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

def test_get_url_icon():
    return

def test_get_default_img():
    with pytest.raises(TypeError):
        urls.get_default_img()
    assert "https://ui-avatars.com/api/?name=testing" == urls.get_default_img(text="testing")
    assert "https://ui-avatars.com/api/?name=test%20ing" == urls.get_default_img(text="test ing")


def test_get_name_by_url():
    with pytest.raises(TypeError):
        urls.get_name_by_url()
    with pytest.raises(ValueError):
        assert "testing" == urls.get_name_by_url(url="testing.com.br")
    assert "testing" == urls.get_name_by_url(url="http://www.testing.com.br")
    assert "testing" == urls.get_name_by_url(url="http://testing.com.br")
    assert "testing" == urls.get_name_by_url(url="http://testing.com")
    assert "google_gservice" == urls.get_name_by_url(url="http://gservice.google.com")
    assert "google_gservice" == urls.get_name_by_url(url="http://subdomain.gservice.google.com")
