import os

from bkmrks import md


def test_md_hr():
    assert md.md_hr() == "\n---"


def test_md_h3_returns_heading_only_for_non_empty_text():
    assert md.md_h3("Work") == "\n### Work"
    assert md.md_h3("") == ""


def test_md_a_img_uses_supplied_name_and_img():
    item = {
        "url": "https://testing.url",
        "name": "name_testing",
        "img": "https://testing.url/favicon.ico",
    }

    assert (
        md.md_a_img(item=item)
        == '\n[![name_testing](https://testing.url/favicon.ico)](https://testing.url "name_testing")'
    )


def test_md_a_img_derives_missing_name_and_default_image(monkeypatch):
    monkeypatch.setattr(md.urlicon, "get_default_img", lambda text: f"default:{text}")

    assert md.md_a_img({"url": "https://docs.example.com/path"}) == (
        '\n[![example_docs](default:example_docs)](https://docs.example.com/path "example_docs")'
    )


def test_md_a_img_returns_empty_string_for_items_without_url():
    assert md.md_a_img({"name": "missing_url", "img": ""}) == ""
    assert md.md_a_img("") == ""


def test_generate_writes_markdown_for_non_empty_catalog(monkeypatch, tmp_path):
    catalog_data = {
        "line0001_work": {
            "item0001": {
                "name": "Docs",
                "url": "https://docs.example.com",
                "img": "https://docs.example.com/icon.png",
            },
            "item0002": {
                "name": "Mail",
                "url": "https://mail.example.com",
                "img": "https://mail.example.com/icon.png",
            },
        },
        "line0002": {
            "item0001": {
                "name": "News",
                "url": "https://news.example.com",
                "img": "https://news.example.com/icon.png",
            }
        },
        "line0003_empty": {},
    }
    monkeypatch.setattr(md.bkmrks, "get_catalog_data", lambda catalog: catalog_data)

    generated_path = md.generate(md_file_name=str(tmp_path / "bookmarks"), catalog="index")

    assert generated_path == str(tmp_path / "bookmarks.md")
    assert (tmp_path / "bookmarks.md").read_text() == (
        "\n### work"
        '\n[![Docs](https://docs.example.com/icon.png)](https://docs.example.com "Docs")'
        '\n[![Mail](https://mail.example.com/icon.png)](https://mail.example.com "Mail")'
        "\n---"
        '\n[![News](https://news.example.com/icon.png)](https://news.example.com "News")'
        "\n---"
    )


def test_generate_uses_default_public_index_path(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))
    monkeypatch.setattr(
        md.bkmrks,
        "get_catalog_data",
        lambda catalog: {
            "line0001": {
                "item0001": {
                    "name": "Docs",
                    "url": "https://docs.example.com",
                    "img": "icon.png",
                }
            }
        },
    )

    generated_path = md.generate(catalog="index")

    assert generated_path == os.path.join(str(tmp_path), "public", "index.md")
    assert os.path.exists(generated_path)


def test_generate_returns_none_for_empty_or_blank_catalog(monkeypatch, tmp_path):
    monkeypatch.setattr(md.bkmrks, "get_catalog_data", lambda catalog: {})

    assert md.generate(md_file_name=str(tmp_path / "empty"), catalog="index") is None
    assert not (tmp_path / "empty.md").exists()

    monkeypatch.setattr(
        md.bkmrks,
        "get_catalog_data",
        lambda catalog: {"line0001_empty": {}},
    )

    assert md.generate(md_file_name=str(tmp_path / "empty_line"), catalog="index") is None
    assert not (tmp_path / "empty_line.md").exists()
