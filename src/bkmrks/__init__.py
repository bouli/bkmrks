import argparse
import os

from bkmrks import bkmrks, presenter


def main():
    parser = argparse.ArgumentParser(prog="bkmrks")
    parser.add_argument("--version", action="version", version="%(prog)s v0.1.3")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    render_parser = subparsers.add_parser(
        "render",
        help="✍️  Render your html bookmarks to public folder.",
    )

    load_parser = subparsers.add_parser(
        "load",
        help="📚 Load and HTML file/url and create a bookmark page.",
    )

    load_parser.add_argument(
        "-html",
        help="HTML file/url to scrape.",
    )

    load_parser.add_argument(
        "-catalog",
        help="Bookmark catalog name.",
    )

    args = parser.parse_args()
    if args.command == "render":
        presenter.render()

    if args.command == "load":
        bkmrks.html2catalog(html_file_name=args.html, catalog=args.catalog)
    return




if __name__ == "__main__":
    main()
