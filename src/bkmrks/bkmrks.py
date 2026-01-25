import os
from urllib.parse import urlparse

import requests
import yaml
from bs4 import BeautifulSoup

from bkmrks import urls


def catalogs_folder():
    return "catalogs"


def get(catalog="index"):
    ensure_catalogs_folder()
    catalog = catalog.split(".")[0] + ".yaml"

    if not os.path.exists(f"{catalogs_folder()}/{catalog}"):
        return {}

    with open(f"{catalogs_folder()}/{catalog}", "r") as f:
        catalog_data = yaml.safe_load(f.read())
        if catalog_data is None:
            return {}
        else:
            return catalog_data


def set(data, catalog="index"):
    ensure_catalogs_folder()
    catalog = catalog.split(".")[0] + ".yaml"
    with open(f"{catalogs_folder()}/{catalog}", "+w") as f:
        yaml.dump(data, f)
        f.seek(0)
    return get(catalog=catalog)


def html2catalog(html_file_name, catalog):
    if str(html_file_name).startswith("https://"):
        html = requests.get(html_file_name).text
        url_parse = urlparse(html_file_name)
        domain = "://".join([url_parse.scheme, url_parse.netloc])

    else:
        domain = ""
        html_file_name = html_file_name.split(".")[0] + ".html"
        with open(html_file_name, "r") as f:
            html = f.read()

    r = BeautifulSoup(html, features="html.parser")
    a = r.find_all(["hr", "a"])

    l = 0
    b = 1
    catalog_data = {}

    for item in a:
        if len(item.attrs) == 0 or l == 0:
            l += 1
            b = 0
            l_name = f"l{l:04d}"

            catalog_data[l_name] = {}
        elif item.has_attr("href") and not item["href"].startswith("#"):
            b += 1
            b_name = f"b{b:04d}"

            item["href"] = urls.ensure_domain(url=item["href"], domain=domain)

            has_img = False
            if len(item.find_all("img")) > 0:
                if len(item.find("img")["src"]) < 200:
                    has_img = False
            if has_img:
                img = item.find("img")["src"]
            else:
                img = urls.get_url_icon(item["href"])
            url = item["href"]
            name = urls.get_name_by_domain(url=url)
            item = {}
            item["name"] = name
            item["url"] = url
            item["img"] = img

            catalog_data[l_name][b_name] = item.copy()

    set(data=catalog_data, catalog=catalog)


def mv_url(
    from_catalog="index",
    from_l=1,
    from_b=0,
    to_catalog="index",
    to_l=1,
    to_b=0,
):
    url = get_url(
        catalog=from_catalog,
        l=from_l,
        b=from_b,
    )
    if url is None:
        return
    add_url(
        url=url,
        catalog=to_catalog,
        l=to_l,
        b=to_b,
    )
    remove_url(
        catalog=from_catalog,
        l=from_l,
        b=from_b,
    )
    return True


def add_url(url, catalog="index", l=1, b=0):
    return edit_bookmark(url=url, catalog=catalog, l=l, b=b, action="add")


def remove_url(catalog="index", l=1, b=0):
    return edit_bookmark(url="", catalog=catalog, l=l, b=b, action="rm")


def edit_bookmark(url, catalog="index", l=1, b=0, action="add"):
    catalog_data = get(catalog=catalog)
    catalog_data_new = {}
    l_name = None
    b_name = None
    if action == "rm" and catalog_data == {}:
        return
    if len(catalog_data) < l and action == "add":
        catalog_data_new = catalog_data.copy()

        l_name = get_l_name(l=len(catalog_data) + 1)
        b_name = get_b_name(b=1)

        catalog_data_new[l_name] = {}
        catalog_data_new[l_name][b_name] = {}
    else:
        l, b = at_least_1(l, b)
        i = 0
        for catalog_l_name, catalog_l in catalog_data.items():
            i += 1
            if len(catalog_l_name) < 4:
                catalog_l_name = get_l_name(l=i)
            if l == i:
                l_name = catalog_l_name
                catalog_data_new[catalog_l_name] = {}
                j = 0
                for catalog_l_b in catalog_l.values():
                    j += 1
                    if b == j and action == "add":
                        catalog_data_new[catalog_l_name][get_b_name(b=j)] = {}
                        b_name = get_b_name(b=j)
                        j += 1
                    if b == j and action == "rm":
                        print("")
                    else:
                        catalog_data_new[catalog_l_name][get_b_name(b=j)] = (
                            catalog_l_b.copy()
                        )
                    print(j)
                if b_name is None and action == "add":
                    j += 1
                    catalog_data_new[catalog_l_name][get_b_name(b=j)] = {}
                    b_name = get_b_name(b=j)
            else:
                catalog_data_new[catalog_l_name] = catalog_l.copy()
    if action != "rm":
        catalog_data_new[l_name][b_name] = parse_url(url=url)

    set(data=catalog_data_new, catalog=catalog)
    return True


def get_url(
    catalog="index",
    l=1,
    b=1,
):
    url = None
    l, b = at_least_1(l, b)
    catalog_data = get(catalog=catalog)
    if len(catalog_data) == 0:
        return
    if len(list(catalog_data.values())) >= l:
        line = list(catalog_data.values())[l - 1]
        if len(list(line.values())) >= b:
            if "url" in list(line.values())[b - 1]:
                url = list(line.values())[b - 1]["url"]

    return url


def get_l_name(l):
    l_name = f"l{l:04d}"
    return l_name


def get_b_name(b):
    b_name = f"b{b:04d}"
    return b_name


def parse_url(url, domain=None):
    if domain is not None:
        url = urls.ensure_domain(url=url, domain=domain)

    name = urls.get_name_by_domain(url=url)

    item = {}
    item["name"] = name
    item["url"] = url
    item["img"] = urls.get_url_icon(url=url)
    return item


def ensure_catalogs_folder():
    if not os.path.exists(catalogs_folder()):
        os.mkdir(catalogs_folder())
        data = {
            "l1": {
                "b1": {
                    "name": "bkmrks_sample_page",
                    "img": "https://cesarcardoso.cc/README/1_bouli.png",
                    "url": "https://github.com/bouli/bkmrks",
                }
            }
        }
        set(data=data)


def at_least_1(l, b):
    if l < 1:
        l = 1
    if b < 1:
        b = 1

    return l, b
