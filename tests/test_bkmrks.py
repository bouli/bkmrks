import os

from bkmrks import bkmrks, folders


def bookmark(name, url=None, img=None):
    return {
        "name": name,
        "url": url or f"https://{name}.example.com",
        "img": img or f"https://{name}.example.com/favicon.ico",
    }


def test_catalog_data_round_trips_yaml_and_missing_catalog_is_empty(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))

    data = {
        "line0001_work": {
            "item0001": bookmark("docs", "https://docs.example.com"),
        }
    }

    assert bkmrks.get_catalog_data("missing") == {}
    assert bkmrks.set_catalog_data(data, catalog="work") == data
    assert bkmrks.get_catalog_data("work.yaml") == data


def test_name_and_index_helpers_preserve_aliases_and_bounds():
    catalog_data = {
        "line0001_work": {
            "item0001": bookmark("docs"),
            "item0002": bookmark("mail"),
        },
        "line0002": {
            "item0001": bookmark("news"),
        },
    }

    assert bkmrks.create_line_name(2) == "line0002"
    assert bkmrks.create_line_name(2, "work") == "line0002_work"
    assert bkmrks.create_item_name(3) == "item0003"
    assert bkmrks.at_least_1(0) == 1
    assert bkmrks.get_dict_key_by_index(2, catalog_data) == "line0002"
    assert bkmrks.get_dict_key_by_index(3, catalog_data) is None
    assert bkmrks.get_alias_from_line_name("line0001_work") == "work"
    assert bkmrks.get_alias_from_line_name("line0001") == ""

    assert bkmrks.get_line_index_alias_from_catalog(1, catalog_data) == (1, "work")
    assert bkmrks.get_line_index_alias_from_catalog(0, catalog_data) == (1, "work")
    assert bkmrks.get_line_index_alias_from_catalog("work", catalog_data) == (1, "work")
    assert bkmrks.get_line_index_alias_from_catalog("new", catalog_data) == (3, "new")

    assert bkmrks.get_item_index_alias_from_catalog(2, 1, catalog_data) == (2, "mail")
    assert bkmrks.get_item_index_alias_from_catalog(0, 1, catalog_data) == (1, "docs")
    assert bkmrks.get_item_index_alias_from_catalog("mail", "work", catalog_data) == (
        2,
        "mail",
    )
    assert bkmrks.get_item_index_alias_from_catalog("missing", "work", catalog_data) == (
        3,
        None,
    )


def test_create_item_from_url_uses_domain_alias_and_icon(monkeypatch):
    monkeypatch.setattr(bkmrks.urlicon, "get_url_icon", lambda url: f"{url}/icon.png")

    assert bkmrks.create_item_from_url(
        url="/docs",
        domain="https://example.com",
        alias="Docs",
    ) == {
        "name": "Docs",
        "url": "https://example.com/docs",
        "img": "https://example.com/docs/icon.png",
    }

    assert bkmrks.create_item_from_url(url="https://python.org") == {
        "name": "python",
        "url": "https://python.org",
        "img": "https://python.org/icon.png",
    }

#TODO: Cover every case
def test_add_remove_and_get_url_update_catalog(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))
    monkeypatch.setattr(bkmrks.urlicon, "get_url_icon", lambda url: "icon.png")

    bkmrks.set_catalog_data(
        {
            "line0001_work": {
                "item0001": bookmark("first", "https://first.example.com"),
                "item0002": bookmark("third", "https://third.example.com"),
            }
        },
        catalog="index",
    )

    assert bkmrks.add_bookmark(
        "https://second.example.com",
        catalog="index",
        line_index="work",
        item_index=2,
        item_alias="Second",
    )
    assert list(bkmrks.get_catalog_data("index")["line0001_work"]) == [
        "item0001",
        "item0002",
        "item0003",
    ]
    assert bkmrks.get_url("index", "work", "Second") == "https://second.example.com"
    assert bkmrks.get_url("index", 1, 3) == "https://third.example.com"

    assert bkmrks.remove_bookmark(catalog="index", line_index="work", item_index="Second")
    assert bkmrks.get_url("index", 1, 2) == "https://third.example.com"
    assert bkmrks.get_url("index", "work", 2) == "https://third.example.com"
    assert bkmrks.get_url("index", "work", "third") == "https://third.example.com"
    assert not bkmrks.remove_bookmark(catalog="index", line_index=9, item_index=1)


def test_add_bookmark_creates_new_alias_line_when_line_does_not_exist(
    monkeypatch, tmp_path
):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))
    monkeypatch.setattr(bkmrks.urlicon, "get_url_icon", lambda url: "icon.png")
    bkmrks.set_catalog_data({}, catalog="index")

    assert bkmrks.add_bookmark(
        "https://docs.example.com",
        catalog="index",
        line_index="work",
        item_index=1,
    )

    assert bkmrks.get_catalog_data("index") == {
        "line0001_work": {
            "item0001": {
                "name": "example_docs",
                "url": "https://docs.example.com",
                "img": "icon.png",
            }
        }
    }


def test_move_bookmark_between_catalogs_refreshes_indexes(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))
    monkeypatch.setattr(bkmrks.urlicon, "get_url_icon", lambda url: "icon.png")
    bkmrks.set_catalog_data(
        {
            "line0001_work": {
                "item0001": bookmark("docs", "https://docs.example.com"),
            }
        },
        catalog="source",
    )
    bkmrks.set_catalog_data(
        {
            "line0001_personal": {
                "item0001": bookmark("blog", "https://blog.example.com"),
            }
        },
        catalog="target",
    )

    assert bkmrks.move_bookmark(
        from_catalog="source",
        from_line_index="work",
        from_item_index="docs",
        to_catalog="target",
        to_line_index="personal",
        to_item_index=1,
    )

    assert bkmrks.get_catalog_data("source") == {"line0001_work": {}}
    assert list(bkmrks.get_catalog_data("target")["line0001_personal"].values()) == [
        {
            "name": "docs",
            "url": "https://docs.example.com",
            "img": "icon.png",
        },
        bookmark("blog", "https://blog.example.com"),
    ]
    assert bkmrks.move_bookmark(
        from_catalog="source",
        from_line_index="work",
        from_item_index=1,
        to_catalog="target",
    ) is None


def test_move_line_between_catalogs_keeps_or_replaces_alias(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))
    bkmrks.set_catalog_data(
        {
            "line0001_work": {"item0001": bookmark("docs")},
            "line0002_later": {"item0001": bookmark("read")},
        },
        catalog="source",
    )
    bkmrks.set_catalog_data(
        {"line0001_personal": {"item0001": bookmark("blog")}},
        catalog="target",
    )

    assert bkmrks.move_line(
        from_catalog="source",
        from_line_index="work",
        to_catalog="target",
        new_line_alias="archive",
    )

    assert bkmrks.get_catalog_data("source") == {
        "line0001_later": {"item0001": bookmark("read")}
    }
    assert list(bkmrks.get_catalog_data("target").items()) == [
        ("line0001_archive", {"item0001": bookmark("docs")}),
        ("line0002_personal", {"item0001": bookmark("blog")}),
    ]


def test_html2catalog_imports_non_anchor_links_with_absolute_urls(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))
    monkeypatch.setattr(
        bkmrks.urls,
        "read_from_url_or_path",
        lambda url_path: """
        <html>
            <body>
                <a href="/docs"><img src="/docs.png">Docs</a>
                <a href="#skip">Skip</a>
                <hr>
                <a href="https://external.example.org/page">External</a>
            </body>
        </html>
        """,
    )
    monkeypatch.setattr(
        bkmrks.urlicon,
        "get_img_from_a_soup_item",
        lambda soup_item, domain: f"icon:{soup_item['href']}",
    )

    bkmrks.html2catalog("https://example.com/bookmarks.html", catalog="imported")

    assert bkmrks.get_catalog_data("imported") == {
        "line0001": {
            "item0001": {
                "name": "example",
                "url": "https://example.com/docs",
                "img": "icon:/docs",
            },
            "item0002": {
                "name": "example_external",
                "url": "https://external.example.org/page",
                "img": "icon:https://external.example.org/page",
            },
        }
    }


def test_clean_catalogs_removes_empty_catalogs_and_keeps_non_empty(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))
    bkmrks.set_catalog_data({"line0001": {}}, catalog="empty")
    bkmrks.set_catalog_data({"line0001": {"item0001": bookmark("docs")}}, catalog="full")

    bkmrks.clean_catalogs()

    assert not os.path.exists(folders.catalogs_folder(path="empty.yaml"))
    assert bkmrks.get_catalog_data("full") == {"line0001": {"item0001": bookmark("docs")}}
