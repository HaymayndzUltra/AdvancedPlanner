import os
import shutil
import tempfile
import pytest


@pytest.fixture()
def tmp_output_dir():
    path = tempfile.mkdtemp(prefix="pipeline_out_")
    try:
        yield path
    finally:
        shutil.rmtree(path, ignore_errors=True)


@pytest.fixture()
def samples_dir() -> str:
    return "/workspace/data/pipelines/samples"