
import os
def apply_extension(file_path:str, ext:str) -> str:
    file_name = ".".join([discard_ext(file_path=file_path)] + [ext])
    file_path = os.path.join(os.path.dirname(file_path), file_name)
    return file_path

def discard_ext(file_path:str):
    file_name = os.path.basename(file_path)
    if file_name == "":
        return file_path

    file_name_elements = file_name.split(".")
    if len(file_name_elements) > 1:
        file_name_elements = file_name_elements[:-1]

    file_name = ".".join(file_name_elements)
    return file_name

def extract_ext(file_path:str):
    file_name = os.path.basename(file_path)
    if file_name == "":
        return file_path

    file_name_elements = file_name.split(".")
    if len(file_name_elements) > 1:
        ext = file_name_elements[-1]
    else:
        ext = ""
    return ext
