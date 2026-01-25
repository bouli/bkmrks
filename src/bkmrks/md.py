from bkmrks import bkmrks


def generate(md_file_name="public/index", yaml_file_name="index"):
    bookmarks = bkmrks.get(file_name=yaml_file_name)
    md_file_content = ""
    if len(bookmarks) > 0:
        for line in bookmarks.values():
            if len(line) > 0:
                for item in line.values():
                    md_file_content += md_a_img(item)
            md_file_content += md_hr()

    md_file_name = md_file_name.split(".")[0] + ".md"
    with open(md_file_name, "+w") as f:
        f.write(md_file_content)
    return md_file_name


def md_a_img(item):
    name = item["name"]
    url = item["url"]
    img = item["img"]

    return f'\n[![{name}]({img})]({url} "{name}")'


def md_hr():
    return "\n---"
