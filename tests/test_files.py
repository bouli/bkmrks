import pytest

from bkmrks import files


@pytest.mark.parametrize(
    ("ext", "file_path", "expected_result"),
    [
        ("yaml", "", ""),
        ("yaml", "/", "/"),
        ("yaml", "/folder/", "/folder/"),
        ("yaml", "/folder/subfolder/", "/folder/subfolder/"),
        ("yaml", "/folder/fi.le.py", "/folder/fi.le.yaml"),
        ("yaml", "/folder/file.py", "/folder/file.yaml"),
        ("yaml", "/folder/file", "/folder/file.yaml"),
        ("yaml", "/file.py", "/file.yaml"),
        ("yaml", "file.py", "file.yaml"),
        ("yaml", "file", "file.yaml"),
        ("yaml", "folder/file.txt", "folder/file.yaml"),
        ("yaml", "./folder/file.txt", "./folder/file.yaml"),
        ("yaml", "archive.tar.gz", "archive.tar.yaml"),
        ("yaml", "file.", "file.yaml"),
        ("yaml", ".env", ""),
    ],
)
def test_apply_ext(ext, file_path, expected_result):
    assert files.apply_ext(ext=ext, file_path=file_path) == expected_result


@pytest.mark.parametrize(
    ("file_path", "expected_result"),
    [
        ("", ""),
        ("/", ""),
        ("/folder/", ""),
        ("/folder/subfolder/", ""),
        ("/folder/fi.le.py", "fi.le"),
        ("/folder/file.py", "file"),
        ("/folder/file", "file"),
        ("/file.py", "file"),
        ("file.py", "file"),
        ("file", "file"),
        ("folder/file.txt", "file"),
        ("./folder/file.txt", "file"),
        ("archive.tar.gz", "archive.tar"),
        ("file.", "file"),
        (".env", ""),
    ],
)
def test_extract_file_name_no_ext(file_path, expected_result):
    assert files.extract_file_name_no_ext(file_path=file_path) == expected_result


@pytest.mark.parametrize(
    ("file_path", "expected_result"),
    [
        ("", ""),
        ("/", ""),
        ("/folder/", ""),
        ("/folder/subfolder/", ""),
        ("/folder/fi.le.py", "py"),
        ("/folder/file.py", "py"),
        ("/folder/file", ""),
        ("/file.py", "py"),
        ("file.py", "py"),
        ("file", ""),
        ("folder/file.txt", "txt"),
        ("./folder/file.txt", "txt"),
        ("archive.tar.gz", "gz"),
        ("file.", ""),
        (".env", "env"),
    ],
)
def test_extract_ext(file_path, expected_result):
    assert files.extract_ext(file_path=file_path) == expected_result


def test_file_helpers_require_arguments():
    with pytest.raises(TypeError):
        files.apply_ext()

    with pytest.raises(TypeError):
        files.extract_file_name_no_ext()

    with pytest.raises(TypeError):
        files.extract_ext()
