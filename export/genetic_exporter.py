import pathlib

import numpy as np
import torch
import pandas as pd

from agents.genetic_agent import GeneticAgent
from export.exporter import Exporter


class GeneticExporter(Exporter):
    """
    Exporter that saves the neural network weights of a evolution agent.
    """

    def __init__(self, path: str):
        super().__init__(path)

    def export(self, agent: GeneticAgent):
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)

        torch.save(agent.neural_network.state_dict(), self.path + "/torch_model")


class GeneticPopulationData:
    """
    Class that encapsulates data to be saved.
    """
    def __init__(self):
        self._generational_data = np.array([[]], dtype=np.float)

    def add_generational_fitness(self, generational_fitness: np.array):
        if self._generational_data.size == 0:
            self._generational_data = generational_fitness.T
        else:
            self._generational_data = np.hstack((self._generational_data, generational_fitness.T))

    def get_generational_data(self) -> np.array:
        return self._generational_data


class GeneticPopulationDataExporter(Exporter):

    def __init__(self, path: str):
        super().__init__(path)
        self._generational_data = np.array([[]], dtype=np.float)

    def export(self, data: GeneticPopulationData):
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)
        fitness_df = pd.DataFrame(data.get_generational_data())
        fitness_df.to_csv(self.path + "/fitness_data.csv")

