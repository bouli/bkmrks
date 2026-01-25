from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


def ensure_domain(url, domain):
    if not url.startswith("https"):
        if url.startswith("/"):
            url = domain + url
        else:
            url = domain + "/" + url
    return url


def get_url_icon(url):
    href_parse = urlparse(url)
    domain = "://".join([href_parse.scheme, href_parse.netloc])
    img = domain + "/favicon.ico"
    try:
        r = requests.get(url)
    except:
        return img

    soup = BeautifulSoup(r.text, features="html.parser")
    soup_link = soup.find_all(
        "link",
        attrs={
            "rel": [
                "icon",
                "apple-touch-icon",
            ]
        },
    )
    if len(soup_link) > 0:
        icon = None
        for icon_item in soup_link:
            if not icon_item.has_attr("sizes"):
                icon_item["sizes"] = "16x16"
            if icon is None:
                icon = icon_item
            else:
                if len(icon_item["sizes"]) < 9:

                    if (
                        len(icon_item["sizes"]) > len(icon_item["sizes"])
                        or icon_item["sizes"].split("x")[0]
                        > icon["sizes"].split("x")[0]
                    ):
                        icon = icon_item
        img = icon["href"]

    img = ensure_domain(url=img, domain=domain)
    if img.split("/")[-1] == "favicon.ico":
        r = requests.get(img)
        if r.status_code == 404:
            if soup.find("img") is None:
                r = requests.get(domain)
                if r.status_code != 404:
                    soup = BeautifulSoup(r.text, features="html.parser")
                    if soup.find("img") is not None:
                        img = soup.find("img")["src"]
            else:
                img = soup.find("img")["src"]
    if not img.startswith("http"):
        if img.startswith("/"):
            separator = ""
        else:
            separator = "/"
        img = separator.join([domain, img])
    return img
