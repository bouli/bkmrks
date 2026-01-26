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
                        img = get_default_img(text=href_parse.netloc)
            else:
                img = soup.find("img")["src"]
    if not img.startswith("http"):
        if img.startswith("/"):
            separator = ""
        else:
            separator = "/"
        img = separator.join([domain, img])
    return img


def get_default_img(text):
    return f"https://ui-avatars.com/api/?name={text}"


def get_name_by_url(url):
    href_parse = urlparse(url)
    name = href_parse.netloc.split(".")

    if name[-2] == "google":
        name = "_".join(name[:-1][::-1])
    else:
        name = name[-2]
    return name

def extract_domain_from_url(url):
    domain = ""

    url_parse = urlparse(url)
    if len(url_parse.netloc)>0:
        domain = "://".join([url_parse.scheme, url_parse.netloc])
    return domain

def read_from_url_or_path(url_path):
    if str(url_path).startswith("https://"):
        content = requests.get(url_path).text

    else:
        url_path = url_path.split(".")[0] + ".html"
        with open(url_path, "r") as f:
            content = f.read()
    return content

def get_img_from_a_soup_item(soup_item, domain):
    soup_item["href"] = ensure_domain(url=soup_item["href"], domain=domain)

    use_soup_img = False
    if len(soup_item.find_all("img")) > 0:
        if len(soup_item.find("img")["src"]) < 200:
            use_soup_img = False
        else:
            use_soup_img = True

    if use_soup_img:
        img = soup_item.find("img")["src"]
    else:
        img = get_url_icon(soup_item["href"])
    return img
