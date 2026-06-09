import pytest

import bkmrks as cli


def run_main(monkeypatch, argv):
    monkeypatch.setattr("sys.argv", ["bkmrks", *argv])
    return cli.main()


def test_main_without_command_returns_without_dispatching(monkeypatch):
    render_calls = []
    monkeypatch.setattr(cli.presenter, "render", lambda: render_calls.append(True))

    assert run_main(monkeypatch, []) is None
    assert render_calls == []


def test_main_version_prints_current_version(monkeypatch, capsys):
    with pytest.raises(SystemExit) as exc_info:
        run_main(monkeypatch, ["--version"])

    assert exc_info.value.code == 0
    assert capsys.readouterr().out == "bkmrks v0.5.5\n"


def test_main_render_dispatches_presenter_render(monkeypatch):
    calls = []
    monkeypatch.setattr(cli.presenter, "render", lambda: calls.append("render"))

    assert run_main(monkeypatch, ["render"]) is None
    assert calls == ["render"]


def test_main_load_imports_html_to_catalog_then_renders(monkeypatch):
    calls = []
    monkeypatch.setattr(
        cli.bkmrks,
        "html2catalog",
        lambda **kwargs: calls.append(("html2catalog", kwargs)),
    )
    monkeypatch.setattr(cli.presenter, "render", lambda: calls.append(("render", {})))

    run_main(monkeypatch, ["load", "bookmarks.html", "-catalog", "work"])

    assert calls == [
        (
            "html2catalog",
            {"html_file_name": "bookmarks.html", "catalog": "work"},
        ),
        ("render", {}),
    ]


def test_main_add_adds_bookmark_then_renders(monkeypatch):
    calls = []
    monkeypatch.setattr(
        cli.bkmrks,
        "add_bookmark",
        lambda **kwargs: calls.append(("add_bookmark", kwargs)),
    )
    monkeypatch.setattr(cli.presenter, "render", lambda: calls.append(("render", {})))

    run_main(
        monkeypatch,
        [
            "add",
            "https://example.com",
            "-catalog",
            "work",
            "-line",
            "dev",
            "-bookmark_item",
            "2",
        ],
    )

    assert calls == [
        (
            "add_bookmark",
            {
                "url": "https://example.com",
                "catalog": "work",
                "line_index": "dev",
                "item_index": "2",
            },
        ),
        ("render", {}),
    ]


def test_main_rm_removes_bookmark_then_renders(monkeypatch):
    calls = []
    monkeypatch.setattr(
        cli.bkmrks,
        "remove_bookmark",
        lambda **kwargs: calls.append(("remove_bookmark", kwargs)),
    )
    monkeypatch.setattr(cli.presenter, "render", lambda: calls.append(("render", {})))

    run_main(
        monkeypatch,
        ["rm", "-catalog", "work", "-line", "dev", "-bookmark_item", "Docs"],
    )

    assert calls == [
        (
            "remove_bookmark",
            {"catalog": "work", "line_index": "dev", "item_index": "Docs"},
        ),
        ("render", {}),
    ]


def test_main_mv_uses_defaults_for_unspecified_move_arguments(monkeypatch):
    calls = []
    monkeypatch.setattr(
        cli.bkmrks,
        "move_bookmark",
        lambda **kwargs: calls.append(("move_bookmark", kwargs)),
    )
    monkeypatch.setattr(cli.presenter, "render", lambda: calls.append(("render", {})))

    run_main(
        monkeypatch,
        ["mv", "-default_catalog", "work", "-default_line", "dev", "-default_bookmark_item", "2"],
    )

    assert calls == [
        (
            "move_bookmark",
            {
                "from_catalog": "work",
                "from_line_index": "dev",
                "from_item_index": "2",
                "to_catalog": "work",
                "to_line_index": "dev",
                "to_item_index": "2",
            },
        ),
        ("render", {}),
    ]


def test_main_mv_overrides_each_move_argument(monkeypatch):
    calls = []
    monkeypatch.setattr(
        cli.bkmrks,
        "move_bookmark",
        lambda **kwargs: calls.append(("move_bookmark", kwargs)),
    )
    monkeypatch.setattr(cli.presenter, "render", lambda: calls.append(("render", {})))

    run_main(
        monkeypatch,
        [
            "mv",
            "-default_catalog",
            "default",
            "-default_line",
            "default_line",
            "-default_bookmark_item",
            "1",
            "-from_catalog",
            "source",
            "-from_line",
            "source_line",
            "-from_bookmark_item",
            "Docs",
            "-to_catalog",
            "target",
            "-to_line",
            "target_line",
            "-to_bookmark_item",
            "3",
        ],
    )

    assert calls == [
        (
            "move_bookmark",
            {
                "from_catalog": "source",
                "from_line_index": "source_line",
                "from_item_index": "Docs",
                "to_catalog": "target",
                "to_line_index": "target_line",
                "to_item_index": "3",
            },
        ),
        ("render", {}),
    ]


def test_main_mvl_uses_default_catalogs_and_line_alias(monkeypatch):
    calls = []
    monkeypatch.setattr(
        cli.bkmrks,
        "move_line",
        lambda **kwargs: calls.append(("move_line", kwargs)),
    )
    monkeypatch.setattr(cli.presenter, "render", lambda: calls.append(("render", {})))

    run_main(
        monkeypatch,
        ["mvl", "-default_catalog", "work", "-line", "dev", "-new_alias", "archive"],
    )

    assert calls == [
        (
            "move_line",
            {
                "from_catalog": "work",
                "from_line_index": "dev",
                "to_catalog": "work",
                "new_line_alias": "archive",
            },
        ),
        ("render", {}),
    ]


def test_main_mvl_overrides_catalogs(monkeypatch):
    calls = []
    monkeypatch.setattr(
        cli.bkmrks,
        "move_line",
        lambda **kwargs: calls.append(("move_line", kwargs)),
    )
    monkeypatch.setattr(cli.presenter, "render", lambda: calls.append(("render", {})))

    run_main(
        monkeypatch,
        [
            "mvl",
            "-default_catalog",
            "default",
            "-from_catalog",
            "source",
            "-line",
            "dev",
            "-to_catalog",
            "target",
        ],
    )

    assert calls == [
        (
            "move_line",
            {
                "from_catalog": "source",
                "from_line_index": "dev",
                "to_catalog": "target",
                "new_line_alias": None,
            },
        ),
        ("render", {}),
    ]
