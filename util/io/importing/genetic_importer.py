import torch
from pysnakegym.model import FFNN

from agents.genetic_agent import GeneticAgent
from util.io.importing.importer import Importer
from pysnakegym.mdp import MDP


class GeneticImporter(Importer):
    """
    Importer that imports a neural network model and makes it available
    """
    def __init__(self, path: str, mdp: MDP, input_dims, n_actions: int):
        """

        :param path: the path of the torch model that will be loaded
        :param mdp: the Mark Decision Process that will be used by the GeneticAgent
        :param input_dims: the input dimensions of the MDP
        :param n_actions: the number actions available in the MDP
        """
        super().__init__(path)
        self.mdp = mdp
        self.input_dims = input_dims
        self.n_actions = n_actions

    def import_model(self) -> GeneticAgent:
        model = torch.load(self.path)
        genetic_agent = GeneticAgent(self.mdp, FFNN(self.__get_layers(model)), 0.0)
        genetic_agent.set_model(model)
        return genetic_agent

    def __get_layers(self, model):
        input = model['input_layer.weight'].shape[1]
        hidden = model['input_layer.weight'].shape[0]
        output = model['output_layer.weight'].shape[0]
        return [input, hidden, output]
