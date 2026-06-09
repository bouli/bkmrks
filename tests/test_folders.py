import os

import yaml
import pytest

from bkmrks import folders, presenter


def test_apply_root_folder_uses_current_directory_by_default(monkeypatch):
    monkeypatch.delenv("BKMRKS_DIR_ROOT", raising=False)

    assert folders.apply_root_folder("public") == "./public/"
    assert folders.apply_root_folder("public", "index.html") == "./public/index.html"


def test_apply_root_folder_uses_configured_root(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))

    assert folders.apply_root_folder("public") == os.path.join(str(tmp_path), "public", "")
    assert folders.apply_root_folder("public", "index.html") == os.path.join(
        str(tmp_path), "public", "index.html"
    )


@pytest.mark.parametrize(
    ("folder_func", "dirname", "subpath"),
    [
        (folders.public_folder, "public", ""),
        (folders.public_folder, "public", "index.html"),
        (folders.templates_folder, "templates", ""),
        (folders.templates_folder, "templates", "index.html"),
        (folders.catalogs_folder, "catalogs", ""),
        (folders.catalogs_folder, "catalogs", "index.yaml"),
    ],
)
def test_folder_helpers_create_and_return_paths(
    monkeypatch, tmp_path, folder_func, dirname, subpath
):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))

    result = folder_func(path=subpath)

    assert os.path.isdir(tmp_path / dirname)
    assert result == os.path.join(str(tmp_path), dirname, subpath)


def test_ensure_public_folder_is_idempotent(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))

    folders.ensure_public_folder()
    folders.ensure_public_folder()

    assert os.path.isdir(tmp_path / "public")


def test_ensure_template_folder_copies_default_templates(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))

    folders.ensure_template_folder()

    copied_templates = sorted(os.listdir(tmp_path / "templates"))
    assert copied_templates == ["index.css", "index.html", "index.js", "menu_item.html"]
    assert "function updateClock()" in (tmp_path / "templates" / "index.js").read_text()


def test_ensure_catalogs_folder_creates_sample_index(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))

    folders.ensure_catalogs_folder()
    folders.ensure_catalogs_folder()

    catalog_path = tmp_path / "catalogs" / "index.yaml"
    catalog_data = yaml.safe_load(catalog_path.read_text())

    assert catalog_data == {
        "line0001": {
            "item0001": {
                "img": "https://cesarcardoso.cc/README/1_bouli.png",
                "name": "bkmrks_sample_page",
                "url": "https://github.com/bouli/bkmrks",
            }
        }
    }


def test_default_templates_include_javascript_for_fresh_root(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))

    html = presenter.get_template("index")

    assert os.path.exists(folders.templates_folder(path="index.js"))
    assert "{js}" not in html
    assert "function updateClock()" in html
