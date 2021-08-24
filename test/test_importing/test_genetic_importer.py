import os
import pathlib
import shutil

import pytest
import torch

from agents.genetic_agent import GeneticAgent
from importing.genetic_importer import GeneticImporter
from rl.mpd import MDP

EXPORTER_PATH = "./test_directory_genetic_importer"

@pytest.fixture
def importer():
    return GeneticImporter(EXPORTER_PATH, MDP(), [4], 4)

@pytest.fixture
def genetic_agent():
    return GeneticAgent(MDP(), 0.1, [4], 4, 0.2)

@pytest.fixture(autouse=True)
def create_and_delete_dir(genetic_agent):
    pathlib.Path(EXPORTER_PATH).mkdir(parents=True, exist_ok=True)
    torch.save(genetic_agent.neural_network.state_dict(), EXPORTER_PATH + "/torch_model")
    assert(os.path.isfile(EXPORTER_PATH + "/torch_model"))

    yield

    if (os.path.isdir(EXPORTER_PATH)):
        shutil.rmtree(EXPORTER_PATH)
    assert(not os.path.isdir(EXPORTER_PATH))

def test_import_model_is_same(importer, genetic_agent):
    loaded_genome = importer.import_model().get_genome()
    expected_genome = genetic_agent.get_genome()

    assert(torch.all(loaded_genome[0].eq(expected_genome[0])))
    assert(torch.all(loaded_genome[1].eq(expected_genome[1])))
    assert(torch.all(loaded_genome[2].eq(expected_genome[2])))