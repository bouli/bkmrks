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
    domain = urls.extract_domain_from_url(url=html_file_name)
    html = urls.read_from_url_or_path(url_path=html_file_name)

    soup = BeautifulSoup(html, features="html.parser")
    soup_hr_a_tags = soup.find_all(["hr", "a"])

    line_index = 0
    item_index = 1
    catalog_data = {}

    for soup_item in soup_hr_a_tags:
        if len(soup_item.attrs) == 0 or line_index == 0:
            line_index += 1
            line_name = get_line_name(line_index=line_index)

            item_index = 0

            catalog_data[line_name] = {}
        elif soup_item.has_attr("href") and not soup_item["href"].startswith("#"):
            item_index += 1
            item_name = get_item_name(item_index=item_index)

            soup_item["href"] = urls.ensure_domain(url=soup_item["href"], domain=domain)

            use_soup_img = False
            if len(soup_item.find_all("img")) > 0:
                if len(soup_item.find("img")["src"]) < 200:
                    use_soup_img = False
                else:
                    use_soup_img = True

            if use_soup_img:
                img = soup_item.find("img")["src"]
            else:
                img = urls.get_url_icon(soup_item["href"])

            url = soup_item["href"]
            name = urls.get_name_by_url(url=url)

            bookmark_item = get_bookmark_item(url=url,name=name,img=img)

            catalog_data[line_name][item_name] = bookmark_item.copy()

    set(data=catalog_data, catalog=catalog)


def mv_url(
    from_catalog="index",
    from_line_index=1,
    from_item_index=0,
    to_catalog="index",
    to_line_index=1,
    to_item_index=0,
):
    url = get_url(
        catalog=from_catalog,
        line_index=from_line_index,
        item_index=from_item_index,
    )
    if url is None:
        return
    add_url(
        url=url,
        catalog=to_catalog,
        line_index=to_line_index,
        item_index=to_item_index,
    )
    remove_url(
        catalog=from_catalog,
        line_index=from_line_index,
        item_index=from_item_index,
    )
    return True


def add_url(url, catalog="index", line_index=1, item_index=0):
    return edit_bookmark(url=url, catalog=catalog, l=line_index, b=item_index, action="add")


def remove_url(catalog="index", line_index=1, item_index=0):
    return edit_bookmark(url="", catalog=catalog, l=line_index, b=item_index, action="rm")


def edit_bookmark(url, catalog="index", line_index=1, item_index=0, action="add"):
    catalog_data = get(catalog=catalog)
    catalog_data_new = {}
    line_name = None
    item_name = None
    if action == "rm" and catalog_data == {}:
        return
    if len(catalog_data) < line_index and action == "add":
        catalog_data_new = catalog_data.copy()

        line_name = get_line_name(line_index=len(catalog_data) + 1)
        item_name = get_item_name(item_index=1)

        catalog_data_new[line_name] = {}
        catalog_data_new[line_name][item_name] = {}
    else:
        line_index = at_least_1(line_index)
        item_index = at_least_1(item_index)
        i = 0
        for catalog_line_name, catalog_line in catalog_data.items():
            i += 1
            if len(catalog_line_name) < 8:
                catalog_line_name = get_line_name(line_index=i)
            if line_index == i:
                line_name = catalog_line_name
                catalog_data_new[catalog_line_name] = {}
                j = 0
                for catalog_line_item in catalog_line.values():
                    j += 1
                    if item_index == j and action == "add":
                        catalog_data_new[catalog_line_name][get_item_name(item_index=j)] = {}
                        item_name = get_item_name(item_index=j)
                        j += 1
                    if item_index == j and action == "rm":
                        print("")
                    else:
                        catalog_data_new[catalog_line_name][get_item_name(item_index=j)] = (
                            catalog_line_item.copy()
                        )
                    print(j)
                if item_name is None and action == "add":
                    j += 1
                    catalog_data_new[catalog_line_name][get_item_name(item_index=j)] = {}
                    item_name = get_item_name(item_index=j)
            else:
                catalog_data_new[catalog_line_name] = catalog_line.copy()
    if action != "rm":
        catalog_data_new[line_name][item_name] = parse_url(url=url)

    set(data=catalog_data_new, catalog=catalog)
    return True


def get_url(
    catalog="index",
    line_index=1,
    item_index=1,
):
    url = None
    line_index = at_least_1(line_index)
    item_index = at_least_1(item_index)

    catalog_data = get(catalog=catalog)
    if len(catalog_data) == 0:
        return
    if len(list(catalog_data.values())) >= line_index:
        catalog_line = list(catalog_data.values())[line_index - 1]
        if len(list(catalog_line.values())) >= item_index:
            if "url" in list(catalog_line.values())[item_index - 1]:
                url = list(catalog_line.values())[item_index - 1]["url"]

    return url


def get_line_name(line_index):
    line_name = f"line{line_index:04d}"
    return line_name


def get_item_name(item_index):
    item_name = f"item{item_index:04d}"
    return item_name


def parse_url(url, domain=None):
    if domain is not None:
        url = urls.ensure_domain(url=url, domain=domain)

    name = urls.get_name_by_url(url=url)

    bookmark_item["img"] = urls.get_url_icon(url=url)
    bookmark_item = get_bookmark_item(url=url, name=name, img=urls.get_url_icon(url=url))
    return bookmark_item

def get_bookmark_item(url, name, img):
    bookmark_item = {}
    bookmark_item["name"] = name
    bookmark_item["url"] = url
    bookmark_item["img"] = img

    return bookmark_item

def ensure_catalogs_folder():
    if not os.path.exists(catalogs_folder()):
        os.mkdir(catalogs_folder())
        data = {
            get_line_name(line_index=1): {
                get_item_name(item_index=1):
                    get_bookmark_item(url="https://github.com/bouli/bkmrks", name="bkmrks_sample_page", img="https://cesarcardoso.cc/README/1_bouli.png")
            }
        }
        set(data=data)


def at_least_1(number):
    number = int(number)
    if number < 1:
        number = 1

    return number
