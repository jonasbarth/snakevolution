import pathlib

import torch

from agents.genetic_agent import GeneticAgent
from export.exporter import Exporter


class GeneticExporter(Exporter):
    """
    Exporter that saves the neural network weights of a genetic agent.
    """
    def __init__(self, path: str):
        super().__init__(path)

    def export(self, agent: GeneticAgent):
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)

        torch.save(agent.neural_network.state_dict(), self.path + "/torch_model")

