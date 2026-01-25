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
        default="index",
    )

    add_parser = subparsers.add_parser(
        "add",
        help="✍️  Add a bookmark to catalog.",
    )

    add_parser.add_argument(
        "url",
        help="URL bookrmark to add to the catalog.",
    )

    add_parser.add_argument(
        "-catalog",
        help="Bookmark catalog name.",
        default="index",
    )

    add_parser.add_argument(
        "-l",
        help="Line of the catalog to add your bookmark.",
        default="1",
    )

    add_parser.add_argument(
        "-pos",
        help="Position in the line of the catalog to add your bookmark.",
        default="0",
    )

    rm_parser = subparsers.add_parser(
        "rm",
        help="❌ Remove a bookmark from catalog.",
    )

    rm_parser.add_argument(
        "-catalog",
        help="Bookmark catalog name.",
        default="index",
    )

    rm_parser.add_argument(
        "-l",
        help="Line of the catalog to add your bookmark.",
        default="1",
    )

    rm_parser.add_argument(
        "-pos",
        help="Position in the line of the catalog to add your bookmark.",
        default="1",
    )



    args = parser.parse_args()
    if args.command == "render":
        presenter.render()

    if args.command == "load":
        bkmrks.html2catalog(html_file_name=args.html, catalog=args.catalog)

    if args.command == "add":
        bkmrks.add_url(url=str(args.url), catalog=str(args.catalog), l=int(args.l), b=int(args.pos))

    if args.command == "rm":
        bkmrks.remove_url(catalog=str(args.catalog), l=int(args.l), b=int(args.pos))
    return




if __name__ == "__main__":
    main()
