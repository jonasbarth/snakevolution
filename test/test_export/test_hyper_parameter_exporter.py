import os
import shutil

import pytest

from export.hyper_parameter_exporter import HyperParameterExporter

EXPORTER_PATH = "./test_directory_hyper_parameter_exporter"


@pytest.fixture
def exporter():
    return HyperParameterExporter(EXPORTER_PATH)


@pytest.fixture
def hyper_parameters():
    keys = ["a", "b", "c", "d", "e"]
    values = [1, "z", 2, "y", 3.0, True]

    return dict(zip(keys, values))


@pytest.fixture(autouse=True)
def delete_dir():
    assert (not os.path.isdir(EXPORTER_PATH))
    yield
    if (os.path.isdir(EXPORTER_PATH)):
        shutil.rmtree(EXPORTER_PATH)
    assert (not os.path.isdir(EXPORTER_PATH))


def test_export_dir_exists(exporter, hyper_parameters):
    exporter.export(hyper_parameters)
    assert (os.path.isdir(EXPORTER_PATH))


def test_torch_model_exists(exporter, hyper_parameters):
    exporter.export(hyper_parameters)
    assert (os.path.isfile(EXPORTER_PATH + "/hyperparameters.json"))

def test_get_path(exporter):
    assert(exporter.get_path() == EXPORTER_PATH)