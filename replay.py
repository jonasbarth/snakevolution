import argparse

from pysnakegym.game import SnakeGameSequencePlayer
from pysnakegym.mdp import SnakeMDP

from util.io.loader import GameSequenceLoader

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--sequence", nargs='?', type=str, default="", help="the path to the pytorch model that will be loaded")
    parser.add_argument("-r", "--record", dest='record', action='store_true', help="indicates whether the game should be recorded or not")
    parser.set_defaults(record=False)

    args = parser.parse_args()
    sequence_path = args.sequence
    record = args.record

    screen_width = 800
    screen_height = 800

    mdp = SnakeMDP(screen_width=screen_width, screen_height=screen_height, snake_size=80, show_game=True)
    importer = GameSequenceLoader(sequence_path)
    sequences = importer.import_sequence()

    player = SnakeGameSequencePlayer(delay=20, record=record, record_path='docs/images')
    for sequence in sequences:
        player.add(sequence)

    player.play()
