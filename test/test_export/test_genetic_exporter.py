import os
import shutil
import pytest

from agents.genetic_agent import GeneticAgent
from export.genetic_exporter import GeneticExporter
from rl.mpd import MDP

EXPORTER_PATH = "./test_directory_genetic_exporter"

@pytest.fixture
def exporter():
    return GeneticExporter(EXPORTER_PATH)

@pytest.fixture
def genetic_agent():
    return GeneticAgent(MDP(), 0.1, [4], 4, 0.2)

@pytest.fixture(autouse=True)
def delete_dir():
    assert(not os.path.isdir(EXPORTER_PATH))
    yield
    if (os.path.isdir(EXPORTER_PATH)):
        shutil.rmtree(EXPORTER_PATH)
    assert(not os.path.isdir(EXPORTER_PATH))

def test_export_dir_exists(exporter, genetic_agent):
    exporter.export(genetic_agent)
    assert(os.path.isdir(EXPORTER_PATH))

def test_torch_model_exists(exporter, genetic_agent):
    exporter.export(genetic_agent)
    assert(os.path.isfile(EXPORTER_PATH + "/torch_model"))

def test_get_path(exporter):
    assert(exporter.get_path() == EXPORTER_PATH)
