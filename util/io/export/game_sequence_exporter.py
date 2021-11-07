import pathlib

import jsonpickle
from pysnakegym.game import GameSequence

from util.io.export import Exporter


class GameSequenceExporter(Exporter):
    """
    Exporter that exports game sequences
    """

    def __init__(self, path: str):
        super().__init__(path)

    def export(self, game_sequences: [GameSequence]):
        pathlib.Path(self.path).mkdir(parents=True, exist_ok=True)

        with open(self.path + "/sequence.json", "w") as outfile:
            outfile.write(jsonpickle.encode(game_sequences))




