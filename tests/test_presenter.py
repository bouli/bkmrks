from pathlib import Path

from bkmrks import folders, presenter


def test_get_file_and_set_variable_replaces_requested_placeholder(tmp_path):
    template_file = tmp_path / "menu_item.html"
    template_file.write_text("<a href='{menu_item}.html'>{menu_item}</a>{other}")

    assert presenter.get_file_and_set_variable(
        file=str(template_file),
        variable="menu_item",
        content="index",
    ) == "<a href='index.html'>index</a>{other}"


def test_get_template_returns_placeholder_when_template_is_missing(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))

    assert presenter.get_template("missing", extension="html") == "{html}"
    assert presenter.get_template("missing", extension="css") == "{css}"


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


def test_set_template_content_replaces_extension_placeholder(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))
    templates_dir = Path(folders.templates_folder())
    (templates_dir / "feed.xml").write_text("<feed>{xml}</feed>")

    assert presenter.set_template_content("<entry />", "feed", extension="xml") == (
        "<feed><entry /></feed>"
    )


def test_generate_html_converts_markdown_with_template_and_catalog(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))
    public_dir = Path(folders.public_folder())
    templates_dir = Path(folders.templates_folder())
    md_file = public_dir / "work.md"

    md_file.write_text("### Work\n\n[Docs](https://docs.example.com)")
    (templates_dir / "custom.html").write_text(
        "<main data-catalog='{__catalog__}'>{html}</main>"
    )

    html_file = presenter.generate_html(str(public_dir / "work"), template="custom")

    assert html_file == str(public_dir / "work.html")
    assert Path(html_file).read_text() == (
        "<main data-catalog='work'><h3>Work</h3>\n"
        '<p><a href="https://docs.example.com">Docs</a></p></main>'
    )


def test_generate_html_uses_default_public_index_path(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))
    public_dir = Path(folders.public_folder())
    (public_dir / "index.md").write_text("hello")

    html_file = presenter.generate_html()

    assert html_file == str(public_dir / "index.html")
    assert "<p>hello</p>" in Path(html_file).read_text()
    assert "menu_selected_index" in Path(html_file).read_text()


def test_clean_public_folder_removes_files_but_ignores_directories(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))
    public_dir = Path(folders.public_folder())
    (public_dir / "old.html").write_text("stale")
    (public_dir / "old.md").write_text("stale")
    (public_dir / "nested").mkdir()

    presenter.clean_public_folder()

    assert not (public_dir / "old.html").exists()
    assert not (public_dir / "old.md").exists()
    assert (public_dir / "nested").is_dir()


def test_delete_files_removes_existing_files_and_ignores_invalid_entries(tmp_path):
    file_to_delete = tmp_path / "delete-me.txt"
    file_to_keep = tmp_path / "keep-me.txt"
    file_to_delete.write_text("delete")
    file_to_keep.write_text("keep")

    presenter.delete_files(
        files=["delete-me.txt", "", "missing.txt", "nested"],
        folder=str(tmp_path),
    )

    assert not file_to_delete.exists()
    assert file_to_keep.exists()


def test_render_outputs_one_html_per_non_empty_catalog_and_menu(monkeypatch, tmp_path):
    monkeypatch.setenv("BKMRKS_DIR_ROOT", str(tmp_path))
    from bkmrks import bkmrks

    bkmrks.set_catalog_data(
        {
            "line0001_work": {
                "item0001": {
                    "img": "work.png",
                    "name": "Docs",
                    "url": "https://docs.example.com",
                }
            }
        },
        catalog="work",
    )
    bkmrks.set_catalog_data(
        {
            "line0001_personal": {
                "item0001": {
                    "img": "personal.png",
                    "name": "Blog",
                    "url": "https://blog.example.com",
                }
            }
        },
        catalog="personal",
    )

    presenter.render()

    public_dir = Path(folders.public_folder())
    work_html = (public_dir / "work.html").read_text()
    personal_html = (public_dir / "personal.html").read_text()

    assert (public_dir / "work.html").exists()
    assert (public_dir / "personal.html").exists()
    assert not (public_dir / "work.md").exists()
    assert not (public_dir / "personal.md").exists()
    assert 'href="work.html"' in work_html
    assert 'href="personal.html"' in work_html
    assert 'id="menu_selected_work"' in work_html
    assert 'href="work.html"' in personal_html
    assert 'href="personal.html"' in personal_html
    assert 'id="menu_selected_personal"' in personal_html


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
