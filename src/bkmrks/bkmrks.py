import os
from urllib.parse import urlparse

import requests
import yaml
from bs4 import BeautifulSoup

from bkmrks.urls import ensure_domain, get_url_icon


def get(file_name="index"):
    ensure_bookmarks_folder()
    file_name = file_name.split(".")[0] + ".yaml"
    with open(f"bookmarks/{file_name}", "r") as f:
        return yaml.safe_load(f.read())


def set_yaml(data, file_name="index"):
    ensure_bookmarks_folder()
    file_name = file_name.split(".")[0] + ".yaml"
    with open(f"bookmarks/{file_name}", "+w") as f:
        yaml.dump(data, f)
        f.seek(0)
    return get(file_name=file_name)


def html2yaml(html_file_name, yaml_file_name):
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
    yaml_data = {}

    for item in a:
        if len(item.attrs) == 0 or l == 0:
            l += 1
            b = 0
            yaml_data[f"l{l}"] = {}
        elif item.has_attr("href") and not item["href"].startswith("#"):
            item["href"] = ensure_domain(url=item["href"], domain=domain)

            b += 1
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

            yaml_data[f"l{l}"][f"b{b}"] = item.copy()

    set_yaml(data=yaml_data, file_name=yaml_file_name)


def ensure_bookmarks_folder():
    if not os.path.exists("bookmarks"):
        os.mkdir("bookmarks")
        data = {
            "l1": {
                "b1": {
                    "name": "bkmrks_page",
                    "img": "https://cesarcardoso.cc/README/1_bouli.png",
                    "url": "https://github.com/bouli/bkmrks",
                }
            }
        }
        set_yaml(data=data)
