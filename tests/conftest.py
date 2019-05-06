import os.path
import pytest


@pytest.fixture(scope="module")
def golden_fit_file():
    path = os.path.join(os.path.dirname(__file__), "golden_file_201903020903.fit")
    handle = open(path, "rb")
    yield handle
    handle.close()
