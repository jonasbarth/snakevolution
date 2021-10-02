import torch

from agents.genetic_agent import GeneticAgent
from util.io.importing import Importer
from rl.mpd import MDP


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
        model = torch.load(self.path + "/torch_model")
        genetic_agent = GeneticAgent(self.mdp, 0.0, self.input_dims, self.n_actions, 0.0)
        genetic_agent.set_model(model)
        return genetic_agent
