import os
from urllib.parse import urlparse

import requests
import yaml
from bs4 import BeautifulSoup

from bkmrks.urls import ensure_domain, get_url_icon

def catalogs_folder():
    return "catalogs"

def get(catalog="index"):
    ensure_catalogs_folder()
    catalog = catalog.split(".")[0] + ".yaml"
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
            catalog_data[f"l{l}"] = {}
        elif item.has_attr("href") and not item["href"].startswith("#"):
            b += 1

            item["href"] = ensure_domain(url=item["href"], domain=domain)

            href_parse = urlparse(item["href"])
            has_img = False
            if len(item.find_all("img")) > 0:
                if len(item.find("img")["src"]) < 200:
                    has_img = False
            if has_img:
                img = item.find("img")["src"]
            else:
                img = get_url_icon(item["href"])
            url = item["href"]
            name = href_parse.netloc.split(".")

            if name[-2] == "google":
                name = "_".join(name[:-1][::-1])
            else:
                name = name[-2]
            item = {}
            item["name"] = name
            item["url"] = url
            item["img"] = img

            catalog_data[f"l{l}"][f"b{b}"] = item.copy()

    set(data=catalog_data, catalog=catalog)

def add_url(url, catalog="index", l=1, b=0):

    return

def parse_url(url, domain=None):
    if domain is not None:
        url = ensure_domain(url=url, domain=domain)

    href_parse = urlparse(url)

    name = href_parse.netloc.split(".")

    if name[-2] == "google":
        name = "_".join(name[:-1][::-1])
    else:
        name = name[-2]
    item = {}
    item["name"] = name
    item["url"] = url
    item["img"] = get_url_icon(url=url)
    return item

def ensure_catalogs_folder():
    if not os.path.exists("catalogs"):
        os.mkdir("catalogs")
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
