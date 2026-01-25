import os

import markdown

def generate_html(md_file="public/index", template="index"):
    ensure_public_folder()
    md_file = md_file.split(".")[0] + ".md"
    with open(md_file, "r") as fm:
        html = set_template_content(
            markdown.markdown(fm.read()), template, extension="html"
        )
        html_file = md_file.split(".")[0] + ".html"
        with open(html_file, "+w") as fh:
            fh.write(html)
    return html_file


def get_file_and_set_variable(file, variable, content):
    with open(file, "r") as f:
        file_content = f.read().replace("{" + variable + "}", content)
    return file_content


def get_template(base_file_name, extension="html"):
    ensure_template_folder()
    template = "{" + extension + "}"

    html_file = "templates/" + base_file_name.split(".")[0] + f".{extension}"
    if os.path.exists(html_file):
        with open(html_file, "r") as f:
            template = f.read()

        if extension == "html":
            dirs = os.listdir("templates")
            for file in dirs:
                if (
                    file.split(".")[1] != "html"
                    and file.split(".")[0] == base_file_name.split(".")[0]
                ):
                    innerextension = file.split(".")[1]
                    innerfile = "templates/" + file
                    with open(innerfile, "r") as f:
                        innertemplate = f.read()
                        template = template.replace(
                            "{" + innerextension + "}", innertemplate
                        )

    return template


def set_template_content(content, base_file_name, extension="html"):
    ensure_template_folder()
    template = get_template(base_file_name, extension=extension)
    return template.replace("{" + extension + "}", content)


def ensure_public_folder():
    if not os.path.exists("public"):
        os.mkdir("public")

def ensure_template_folder():
    if not os.path.exists("templates"):
        os.mkdir("templates")
        default_templates_dir = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "templates"
        )
        files = os.listdir(default_templates_dir)
        for file in files:
            if file.split(".")[1] in ["css","html"]:
                with open(os.path.join(default_templates_dir,file),"r+") as fr:
                    with open(os.path.join("templates",file),"+w") as fw:
                        fw.write(fr.read())
