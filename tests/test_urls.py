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
    return
