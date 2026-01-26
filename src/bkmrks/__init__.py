import argparse
import os

from bkmrks import bkmrks, presenter


def main():
    parser = argparse.ArgumentParser(prog="bkmrks")
    parser.add_argument("--version", action="version", version="%(prog)s v0.2.0")

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
        help="Line of the catalog to remove your bookmark.",
        default="1",
    )

    rm_parser.add_argument(
        "-pos",
        help="Position in the line of the catalog to remove your bookmark.",
        default="1",
    )

    mv_parser = subparsers.add_parser(
        "mv",
        help="🔄 Move a bookmark from a catalog to another.",
    )

    mv_parser.add_argument(
        "-f_catalog",
        help="Bookmark catalog name to move from.",
        default="index",
    )

    mv_parser.add_argument(
        "-f_l",
        help="Line of the catalog to move from.",
        default="1",
    )

    mv_parser.add_argument(
        "-f_pos",
        help="Position in the line of the catalog to move from.",
        default="1",
    )

    mv_parser.add_argument(
        "-t_catalog",
        help="Bookmark catalog name to move to.",
        default="index",
    )

    mv_parser.add_argument(
        "-t_l",
        help="Line of the catalog to move to.",
        default="1",
    )

    mv_parser.add_argument(
        "-t_pos",
        help="Position in the line of the catalog to move to.",
        default="1",
    )

    args = parser.parse_args()
    if args.command == "render":
        presenter.render()

    if args.command == "load":
        bkmrks.html2catalog(html_file_name=args.html, catalog=args.catalog)

    if args.command == "add":
        bkmrks.add_url(
            url=str(args.url), catalog=str(args.catalog), line_index=int(args.l), item_index=int(args.pos)
        )

    if args.command == "rm":
        bkmrks.remove_url(catalog=str(args.catalog), line_index=int(args.l), item_index=int(args.pos))

    if args.command == "mv":
        bkmrks.mv_url(
            from_catalog=args.f_catalog,
            from_line_index=args.f_l,
            from_item_index=args.f_pos,
            to_catalog=args.to_catalog,
            to_line_index=args.to_l,
            to_item_index=args.to_pos,
        )
    return


if __name__ == "__main__":
    main()
