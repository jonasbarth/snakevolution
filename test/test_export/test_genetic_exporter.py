import os
import shutil
import numpy as np
import pytest

from agents.genetic_agent import GeneticAgent
from util.io.export.genetic_exporter import GeneticExporter, GeneticPopulationDataExporter, GeneticPopulationData
from rl.mpd import MDP

EXPORTER_PATH = "./test_directory_genetic_exporter"


@pytest.fixture
def exporter():
    return GeneticExporter(EXPORTER_PATH)


@pytest.fixture
def genetic_agent():
    return GeneticAgent(MDP(), 0.1, [4], 4, 0.2)


def test_export_dir_exists(exporter, genetic_agent):
    exporter.export(genetic_agent)
    assert (os.path.isdir(EXPORTER_PATH))


def test_torch_model_exists(exporter, genetic_agent):
    exporter.export(genetic_agent)
    assert (os.path.isfile(EXPORTER_PATH + "/torch_model"))


def test_get_path(exporter):
    assert (exporter.get_path() == EXPORTER_PATH)


@pytest.fixture
def genetic_population_data():
    return GeneticPopulationData()


def test_append_data(genetic_population_data):
    data = np.array([[1, 2, 3, 4, 5]])
    data2 = np.array([[7, 8, 9, 10, 6]])
    genetic_population_data.add_generational_fitness(data)
    genetic_population_data.add_generational_fitness(data2)
    assert (genetic_population_data.get_generational_data() == np.hstack((data.T, data2.T))).all()


POPULATION_EXPORTER_PATH = "./test_directory_genetic_population_data_exporter"

@pytest.fixture
def genetic_population_data_exporter():
    return GeneticPopulationDataExporter(POPULATION_EXPORTER_PATH)


def test_save_data(genetic_population_data, genetic_population_data_exporter):
    genetic_population_data.add_generational_fitness(np.array([[1, 2, 3, 4, 5]]))
    genetic_population_data_exporter.export(genetic_population_data)
    assert (os.path.isfile(POPULATION_EXPORTER_PATH + "/fitness_data.csv"))


@pytest.fixture(autouse=True)
def delete_dir():
    assert (not os.path.isdir(EXPORTER_PATH))
    assert (not os.path.isdir(POPULATION_EXPORTER_PATH))
    yield
    if (os.path.isdir(EXPORTER_PATH)):
        shutil.rmtree(EXPORTER_PATH)
    if (os.path.isdir(POPULATION_EXPORTER_PATH)):
        shutil.rmtree(POPULATION_EXPORTER_PATH)
    assert (not os.path.isdir(EXPORTER_PATH))
    assert (not os.path.isdir(POPULATION_EXPORTER_PATH))

