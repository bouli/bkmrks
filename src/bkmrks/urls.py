import urllib

import requests

def ensure_domain(url, domain):
    if urllib.parse.urlparse(url).netloc == '' and urllib.parse.urlparse(domain).netloc == '':
        raise ValueError("`url` or `domain` must be a domain")

    if urllib.parse.urlparse(url).netloc == "":
        parsed_url = urllib.parse.urlparse(url)
        parsed_domain = urllib.parse.urlparse(domain)
        url = parsed_url._replace(scheme="https",netloc=parsed_domain.netloc).geturl()

    url = urllib.parse.urlparse(url)._replace(scheme="https").geturl()
    return url


def get_name_from_domain(url):
    href_parse = urllib.parse.urlparse(url)
    country_code_len = 2

    if href_parse.netloc == "":
        raise ValueError("`url` must have a domain")
    name = href_parse.netloc.split(".")

    if len(name[-1]) == country_code_len:
        name = name[:-1]

    if name[0] == "www":
        name = name[1:]

    if len(name) > 2:
        name = "_".join(name[-3:-1][::-1])
    else:
        name = name[-2]
    return name


def extract_domain_from_url(url):
    domain = ""

    url_parse = urllib.parse.urlparse(url)
    if len(url_parse.netloc) > 0:
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
