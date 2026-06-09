from pathlib import Path

from bkmrks import folders, presenter


def test_get_template_inlines_same_base_assets_by_extension(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))
    templates_dir = Path(folders.templates_folder())

    (templates_dir / "custom.html").write_text(
        "<style>{css}</style><script>{js}</script><aside>{asset}</aside>{html}"
    )
    (templates_dir / "custom.css").write_text(".custom { color: red; }")
    (templates_dir / "custom.js").write_text("window.customTemplate = true;")
    (templates_dir / "custom.asset").write_text("custom asset content")
    (templates_dir / "other.css").write_text("other css should not leak")
    (templates_dir / "other.js").write_text("other js should not leak")
    (templates_dir / "other.asset").write_text("other asset should not leak")

    html = presenter.set_template_content(
        "<main>bookmark content</main>", "custom", extension="html"
    )

    assert ".custom { color: red; }" in html
    assert "window.customTemplate = true;" in html
    assert "custom asset content" in html
    assert "<main>bookmark content</main>" in html
    assert "other css should not leak" not in html
    assert "other js should not leak" not in html
    assert "other asset should not leak" not in html
    assert "{css}" not in html
    assert "{js}" not in html
    assert "{asset}" not in html
    assert "{html}" not in html


def test_fresh_render_outputs_html_without_unresolved_template_assets(
    monkeypatch, tmp_path
):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))

    presenter.render()

    html_file = Path(folders.public_folder(path="index.html"))
    assert html_file.exists()

    html = html_file.read_text()
    assert "{js}" not in html
    assert "{css}" not in html
    assert "{html}" not in html
    assert "{menu}" not in html
    assert "/* index.css */" in html
    assert "function updateClock()" in html
    assert "bkmrks_sample_page" in html
    assert 'id="menu_selected_index"' in html
