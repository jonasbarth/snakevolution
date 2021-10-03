import argparse

from util.io.importing.genetic_importer import GeneticImporter
from pysnakegym.mdp import SnakeMDP

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-m", "--model", nargs='?', type=str, default="", help="the path to the pytorch model that will be loaded")
    args = parser.parse_args()

    model_path = args.model

    mdp = SnakeMDP(show_game=True)
    importer = GeneticImporter(model_path, mdp, [mdp.state_dims()[0]], mdp.n_actions())
    genetic_agent = importer.import_model()

    state, reward, done = mdp.reset()

    while not done:
        action = genetic_agent.choose_action(state)
        state_, reward, done = mdp.step(action=action)
        state = state_
