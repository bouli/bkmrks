import argparse
import os

from bkmrks import bkmrks, md, presenter


def main():
    parser = argparse.ArgumentParser(prog="bkmrks")
    parser.add_argument("--version", action="version", version="%(prog)s v0.1.1")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    render_parser = subparsers.add_parser(
        "render",
        help="✍️ Render your html bookmarks to public folder.",
    )

    load_parser = subparsers.add_parser(
        "load",
        help="✍️ Load and HTML file/url and create a bookmark page.",
    )

    load_parser.add_argument(
        "-h",
        help="HTML file/url to scrape.",
    )

    load_parser.add_argument(
        "-b",
        help="Bookmark catalog name.",
    )

    args = parser.parse_args()
    if args.command == "render":
        render()

    if args.command == "render":
        bkmrks.html2yaml(html_file_name=args.h, yaml_file_name=args.b)
    return


def render():
    bkmrks.ensure_bookmarks_folder()
    presenter.ensure_public_folder()

    bookmarks = os.listdir("bookmarks")
    menu = []
    htmls = []
    for bookmark in bookmarks:
        md_file_name = "public/" + bookmark
        md.generate(md_file_name=md_file_name, yaml_file_name=bookmark)
        htmls.append(presenter.generate_html(md_file_name))
        menu.append(
            presenter.get_file_and_set_variable(
                file="templates/menu_item.html",
                variable="menu_item",
                content=bookmark.split(".")[0],
            )
        )
    menu = " | ".join(menu)
    for html in htmls:
        html_content = presenter.get_file_and_set_variable(
            file=html,
            variable="menu",
            content=menu,
        )
        with open(html, "+w") as f:
            f.write(html_content)


if __name__ == "__main__":
    main()
