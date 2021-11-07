import jsonpickle
from pysnakegym.game import GameSequence

from util.io.loader import Loader


class GameSequenceLoader(Loader):
    """
    Importer that imports a list of GameSequences so that they can be replayed
    """
    def __init__(self, path: str):
        super().__init__(path)

    def import_sequence(self) -> [GameSequence]:
        file = open(self.path)
        json_str = file.read()
        return jsonpickle.decode(json_str)
