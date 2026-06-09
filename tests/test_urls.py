import pytest

from bkmrks import urls


@pytest.mark.parametrize(
    ("url", "domain", "expected_result"),
    [
        ("", "https://domain.com", "https://domain.com"),
        ("/", "https://domain.com", "https://domain.com/"),
        ("?param=1", "https://domain.com", "https://domain.com?param=1"),
        ("/?param=1", "https://domain.com", "https://domain.com/?param=1"),
        ("#anchor", "https://domain.com", "https://domain.com#anchor"),
        ("/#anchor", "https://domain.com", "https://domain.com/#anchor"),
        ("path", "https://domain.com", "https://domain.com/path"),
        ("/path", "https://domain.com", "https://domain.com/path"),
        (
            "https://domain.com/path",
            "https://otherdomain.com",
            "https://domain.com/path",
        ),
        ("http://domain.com/path", "", "https://domain.com/path"),
        ("/path", "http://domain.com/other-path", "https://domain.com/path"),
        ("/path?x=1#top", "https://domain.com/base", "https://domain.com/path?x=1#top"),
    ],
)
def test_ensure_domain(url, domain, expected_result):
    assert urls.ensure_domain(url=url, domain=domain) == expected_result


def test_ensure_domain_requires_url_and_valid_domain():
    with pytest.raises(TypeError):
        urls.ensure_domain(url="/path")

    with pytest.raises(ValueError):
        urls.ensure_domain(url="/path", domain="not-a-domain.com")


@pytest.mark.parametrize(
    ("url", "expected_result"),
    [
        ("http://www.testing.com.br", "testing"),
        ("http://testing.com.br", "testing"),
        ("http://testing.com", "testing"),
        ("http://testing.cc", "testing"),
        ("http://gservice.google.com", "google_gservice"),
        ("http://subdomain.gservice.google.com", "google_gservice"),
        ("https://localhost", "localhost"),
        ("https://docs.python.org/3/library/urllib.parse.html", "python_docs"),
    ],
)
def test_get_name_from_domain(url, expected_result):
    assert urls.get_name_from_domain(url=url) == expected_result


def test_get_name_from_domain_requires_absolute_url():
    with pytest.raises(TypeError):
        urls.get_name_from_domain()

    with pytest.raises(ValueError):
        urls.get_name_from_domain(url="testing.com.br")


@pytest.mark.parametrize(
    ("url", "expected_result"),
    [
        ("http://www.testing.com.br", "http://www.testing.com.br"),
        (
            "http://www.testing.com.br/path?param1#anchor",
            "http://www.testing.com.br",
        ),
        ("https://testing.com:8443/path", "https://testing.com:8443"),
        ("www.testing.com.br", ""),
        ("/asdf", ""),
        ("", ""),
    ],
)
def test_extract_domain_from_url(url, expected_result):
    assert urls.extract_domain_from_url(url=url) == expected_result


def test_extract_domain_from_url_requires_argument():
    with pytest.raises(TypeError):
        urls.extract_domain_from_url()


def test_read_from_url_or_path_reads_https_url(monkeypatch):
    class Response:
        text = "<html>remote</html>"

    requested_urls = []

    def fake_get(url):
        requested_urls.append(url)
        return Response()

    monkeypatch.setattr(urls.requests, "get", fake_get)

    assert urls.read_from_url_or_path("https://example.com/bookmarks.html") == (
        "<html>remote</html>"
    )
    assert requested_urls == ["https://example.com/bookmarks.html"]


def test_read_from_url_or_path_returns_empty_string_when_request_fails(monkeypatch):
    def fake_get(url):
        raise urls.requests.RequestException("network unavailable")

    monkeypatch.setattr(urls.requests, "get", fake_get)

    assert urls.read_from_url_or_path("https://example.com/bookmarks.html") == ""


def test_read_from_url_or_path_reads_local_html_with_normalized_extension(tmp_path):
    html_file = tmp_path / "bookmarks.html"
    html_file.write_text("<html>local</html>")

    assert urls.read_from_url_or_path(str(tmp_path / "bookmarks.md")) == (
        "<html>local</html>"
    )


@pytest.mark.parametrize(
    ("path", "url", "expected_result"),
    [
        ("/assets/icon.png", "http://example.com/page.html", "https://example.com/assets/icon.png"),
        (
            "https://cdn.example.com/icon.png",
            "https://example.com/page.html",
            "https://cdn.example.com/icon.png",
        ),
        (
            "assets/icon.png",
            "https://example.com/folder/page.html?x=1#top",
            "https://example.com/folder/assets/icon.png",
        ),
        (
            "assets/icon.png",
            "https://example.com/folder/",
            "https://example.com/folder//assets/icon.png",
        ),
        (
            "assets/icon.png",
            "https://example.com/folder",
            "https://example.com/folder/assets/icon.png",
        ),
    ],
)
def test_ensure_relative_path(path, url, expected_result):
    assert urls.ensure_relative_path(path=path, url=url) == expected_result


def test_ensure_relative_path_requires_non_empty_path():
    with pytest.raises(IndexError):
        urls.ensure_relative_path(path="", url="https://example.com")
