from src.uploadgsp.util import write_str_to_file, read_str_from_file
import pytest
import os


@pytest.mark.parametrize(
    ("file", "s"),
    [
        ("test_write_str_to_file", "a"),
        ("test_write_str_to_file", "b"),
        ("test_write_str_to_file", "c"),
    ],
)
def test_write_str_to_file(file, s: str):
    write_str_to_file(file, s)

    with open(
        file=file,
        mode="r",
        encoding="UTF-8",
    ) as f:
        assert f.read() == s
        os.remove(file)


@pytest.mark.parametrize(
    ("file", "s"),
    [
        ("test_read_str_from_file", "a"),
        ("test_read_str_from_file", "b"),
        ("test_read_str_from_file", "c"),
    ],
)
def test_read_str_from_file(file, s):
    with open(
        file=file,
        mode="w",
        encoding="UTF-8",
    ) as f:
        f.write(s)
    assert read_str_from_file(f.name) == s
    os.remove(file)
