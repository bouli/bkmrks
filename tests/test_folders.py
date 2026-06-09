import os

from bkmrks import folders, presenter


def test_default_templates_include_javascript_for_fresh_root(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))

    html = presenter.get_template("index")

    assert os.path.exists(folders.templates_folder(path="index.js"))
    assert "{js}" not in html
    assert "function updateClock()" in html
